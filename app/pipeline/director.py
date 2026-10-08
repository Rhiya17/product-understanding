"""Claude in the video pipeline: a Director that plans shots and a Critic that
reviews the finished video against the customer's question.

    request → Director (plan) → validate → Executor (FAL) → Critic → publish
                   ↑                                           │
                   └──────────── one re-plan with notes ───────┘

Claude makes the judgment calls a person used to make by hand: which devices
the question involves, which official photo and crop show each step, which
motion to generate, and whether the result actually answers the question.
Code keeps the rules: Claude may only reference verified step claims and
official vault photos, every step must be shot or explicitly listed as not
shown, spending is reserved before every call, and the Critic's verdict is
re-checked deterministically before anything is published.
"""
import base64
import io
import json
import re
from pathlib import Path
from typing import List, Literal

from pydantic import BaseModel, Field

from app.pipeline.store import REPO_ROOT

MODEL = "claude-opus-5"
MAX_TOKENS = 10000
MAX_SHOTS = 3
MAX_MANUAL_PAGES = 6
CROP_ASPECT = (1.3, 2.0)          # the generated frame is 16:9; wider crops get black bars
MAX_PHOTOS_PER_PRODUCT = 24      # the right photo is often not among the first few
CRITIC_FRAMES = 12
# Worst case per call at claude-opus-5 list prices ($5 in / $25 out per MTok):
# ~45k input tokens (text + up to ~40 downscaled photos) and MAX_TOKENS output.
CLAUDE_CALL_WORST_USD = 45_000 * 5 / 1e6 + MAX_TOKENS * 25 / 1e6


# ---------------------------------------------------------------- schemas

class Shot(BaseModel):
    step_claim_ids: List[str] = Field(description="Verified step claims this shot demonstrates, in order.")
    device_product_dir: str = Field(description="Catalog product whose official photo is used.")
    photo_id: str = Field(description="source_id of one official photo of that product.")
    crop: List[int] = Field(description="[x0, y0, x1, y1] in the photo's original pixels, or [] for the whole photo.")
    strategy: Literal["reverse_from_after_photo", "forward_from_before_photo"]
    motion_prompt: str = Field(description="What moves, from the camera's point of view. No text overlays.")
    must_be_visible: List[str] = Field(description="Concrete things a reviewer must see for this shot to count.")


class NotShown(BaseModel):
    claim_id: str
    reason: str


class ShotPlan(BaseModel):
    devices_involved: List[str]
    shots: List[Shot]
    not_shown: List[NotShown]
    notes: str


class StepVerdict(BaseModel):
    claim_id: str
    shown: bool
    evidence: str


class ShotVerdict(BaseModel):
    shot: int
    approved: bool = Field(description="This shot alone is correct: right part, right place, nothing invented or changing.")
    issues: List[str]


class Critique(BaseModel):
    answers_the_question: bool
    steps: List[StepVerdict]
    shots: List[ShotVerdict] = Field(default_factory=list, description="One verdict per shot, in order.")
    devices_correct: bool
    invented_or_wrong: List[str] = Field(description="Parts, ports, labels or changes that contradict the official photos.")
    verdict: Literal["pass", "fail"]
    fix_notes: str = Field(description="Specific changes for a re-plan if the verdict is fail.")


class ShotCheck(BaseModel):
    shot: int
    part_in_frame: bool = Field(description="The part the step acts on is clearly visible in this exact starting frame, where the manual shows it.")
    state_matches_strategy: bool = Field(description="reverse: the frame shows the step already done; forward: the frame shows the state before the step.")
    motion_matches_manual: bool
    issues: List[str]


class PlanCheck(BaseModel):
    shots: List[ShotCheck]
    covers_the_question: bool
    approve: bool
    fix_notes: str


class PlanRejected(ValueError):
    pass


# ---------------------------------------------------------------- inputs

def catalog():
    return json.loads((REPO_ROOT / "source-vault" / "catalog.json").read_text())["products"]


def mentioned_products(question, primary):
    """Other catalog products the question names (a word is a prefix of a name word)."""
    words = {w for w in re.findall(r"[a-z0-9]+", (question or "").lower()) if len(w) >= 3}
    found = []
    for product in catalog():
        if product["dir"] == primary:
            continue
        names = re.findall(r"[a-z0-9]+", f"{product['brand']} {product['model']}".lower())
        if any(n.startswith(w) for w in words for n in names if len(n) >= 3):
            found.append(product["dir"])
    return sorted(found)


def official_photos(product_dir):
    vault = REPO_ROOT / "source-vault" / product_dir
    manifest = json.loads((vault / "manifest.json").read_text())
    photos = []
    for source in manifest.get("sources", []):
        path = vault / str(source.get("local_path", ""))
        if source.get("type") == "IMAGE" and path.is_file():
            photos.append({"photo_id": source["source_id"], "path": path,
                           "title": source.get("title") or path.stem.replace("-", " ")})
    return photos[:MAX_PHOTOS_PER_PRODUCT]


def image_block(path, crop=None, max_side=768):
    from PIL import Image
    image = Image.open(path).convert("RGBA")
    flat = Image.new("RGB", image.size, "white")
    flat.paste(image, mask=image.split()[3])
    if crop:
        flat = flat.crop(tuple(crop))
    flat.thumbnail((max_side, max_side))
    buffer = io.BytesIO()
    flat.save(buffer, "JPEG", quality=85)
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                        "data": base64.standard_b64encode(buffer.getvalue()).decode()}}


def manual_page_images(product_dir, steps):
    """Rendered manual pages the steps (and their parts) cite: where things really are."""
    from app.server import render_pdf_page
    vault = REPO_ROOT / "source-vault" / product_dir
    sources = {s["source_id"]: s for s in json.loads((vault / "manifest.json").read_text())["sources"]}
    pages, seen = [], set()
    required = list(dict.fromkeys(tuple(page) for step in steps
                                  for page in step.get("required_manual_pages", [])))
    if len(required) > MAX_MANUAL_PAGES:
        raise ValueError("Required manual evidence exceeds the video reference limit")
    ordered = required + [page for step in steps for page in step.get("manual_pages", [])]
    for source_id, page in ordered:
        source = sources.get(source_id)
        if (source_id, page) in seen:
            continue
        if not source or not str(source.get("local_path", "")).endswith(".pdf"):
            if (source_id, page) in required:
                raise ValueError(f"Required manual reference is unavailable: {source_id}, page {page}")
            continue
        seen.add((source_id, page))
        path = render_pdf_page(vault / source["local_path"], page,
                               REPO_ROOT / "app" / "cache" / "pdf-pages", source.get("sha256"))
        pages.append((source_id, page, path))
    return pages[:MAX_MANUAL_PAGES]


def manual_blocks(product_dir, steps):
    blocks = []
    for source_id, page, path in manual_page_images(product_dir, steps):
        blocks.append({"type": "text", "text": f"Manufacturer manual {source_id}, page {page} "
                                               "(ground truth for where parts are and how they move):"})
        blocks.append(image_block(path, max_side=900))
    return blocks


def photo_size(path):
    from PIL import Image
    with Image.open(path) as image:
        return image.size


# ---------------------------------------------------------------- Claude calls

DIRECTOR_SYSTEM = """\
You are the director of short how-to videos for a product-help app. Every video must
answer the customer's exact question using only verified manufacturer steps and
official product photos. A generator turns each of your shots into a 4-second clip by
animating one official photo; it can invent details, so choose photos and crops that
make each step's key part large and unambiguous.

Rules:
- Cover every step: put each step's claim_id in exactly one shot, or in not_shown with
  a reason (for example, no official photo shows the part, or the step is a software
  screen). Never drop a step silently.
- A step that happens on another device (e.g. "the source device") must be shown on
  the device the customer named, if its photos are provided.
- Use at most {max_shots} shots. Group consecutive steps that one photo can show.
- reverse_from_after_photo: the photo shows the step already done (e.g. a cable
  plugged in). The generator animates undoing it and the clip is played backwards,
  so the last frame is the real photo. Prefer this whenever such a photo exists.
- forward_from_before_photo: the photo shows the state before the step; the generator
  animates the step forward. Describe exactly where the motion ends.
- Avoid photos with text labels, callout lines or several products side by side,
  unless a crop removes them. Crops are in the photo's original pixels.
- The generated video is 16:9. Every crop (or the whole photo if uncropped) must have
  a width:height ratio between 1.3 and 2.0.
- Where a part is and which way things move come from the manual pages provided.
  Make each motion_prompt name the exact location (e.g. "the round port on the
  bottom edge of the left earcup") so the generator cannot put it somewhere else.
- motion_prompt: static camera, the product never changes shape, color or logos,
  no hands unless needed, no on-screen text.
"""

CRITIC_SYSTEM = """\
You review a generated how-to video before a customer sees it. Be strict: a video
that looks good but skips a step, shows the wrong device, or changes the product is a
fail. Judge only what is visible in the frames. Compare products against the official
photos and manual pages provided: a port with the wrong shape (round vs oval slot) or in
the wrong position counts as invented. For every step claimed to be shown, decide
whether it is clearly visible, and give every shot its own verdict: a shot is approved
only if it has no issue at all. If you fail the video, write fix_notes a director can act on.
"""


def claude_client():
    import anthropic
    return anthropic.Anthropic()


def call_claude(client, system, content, schema, budget, job_id, label):
    reservation = budget.reserve(job_id, f"anthropic/{MODEL} {label}", CLAUDE_CALL_WORST_USD)
    import anthropic
    try:
        response = _parse(client, system, content, schema)
    except anthropic.APIStatusError:
        budget.settle(reservation, 0.0)       # rejected requests (4xx/5xx) are not billed
        raise
    return _finish(response, budget, reservation, label)


def _parse(client, system, content, schema):
    return client.beta.messages.parse(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        system=system,
        messages=[{"role": "user", "content": content}],
        output_format=schema,
    )


def _finish(response, budget, reservation, label):
    usage = response.usage
    budget.settle(reservation, usage.input_tokens * 5 / 1e6 + usage.output_tokens * 25 / 1e6
                  + (getattr(usage, "cache_creation_input_tokens", 0) or 0) * 6.25 / 1e6
                  + (getattr(usage, "cache_read_input_tokens", 0) or 0) * 0.5 / 1e6)
    if response.stop_reason == "refusal":
        raise RuntimeError(f"Claude declined the {label} request")
    if response.stop_reason == "max_tokens" or response.parsed_output is None:
        raise RuntimeError(f"Claude's {label} response was incomplete")
    return response.parsed_output, {"model": response.model,
                                    "input_tokens": response.usage.input_tokens,
                                    "output_tokens": response.usage.output_tokens,
                                    "request_id": getattr(response, "_request_id", None)}


def plan_shots(client, budget, job_id, question, product, steps, devices, critique=None,
               approved=()):
    content = [{"type": "text", "text": (
        f"Customer question: {question}\n"
        f"Product: {product['name']} ({product['dir']})\n"
        f"Other products the question names: {', '.join(devices) or 'none'}\n\n"
        "Verified steps (claim_id — step — manufacturer quote — parts):\n" + "\n".join(
            f"{s['claim_id']} — {s['text']} — \"{s.get('quote', '')}\" — "
            f"{', '.join(s['parts']) or 'no product part'}" for s in steps))}]
    for product_dir in [product["dir"]] + devices:
        for photo in official_photos(product_dir):
            width, height = photo_size(photo["path"])
            content.append({"type": "text", "text": (
                f"Official photo — product {product_dir}, photo_id {photo['photo_id']}, "
                f"{width}x{height}px, title: {photo['title']}")})
            content.append(image_block(photo["path"]))
    content.extend(manual_blocks(product["dir"], steps))
    if approved:
        content.append({"type": "text", "text": (
            "These shots were already generated and approved by review. Reuse them exactly "
            "(copy each as a shot, unchanged) and plan only the steps they do not cover:\n"
            + json.dumps(list(approved), indent=1))})
    if critique:
        content.append({"type": "text", "text": (
            "Your previous plan produced a video that failed review. Reviewer notes:\n"
            f"{critique.fix_notes}\nInvented or wrong: {critique.invented_or_wrong}\n"
            "Make a new plan that fixes these. Keep any shot that was not criticised "
            "exactly as it was.")})
    return call_claude(client, DIRECTOR_SYSTEM.format(max_shots=MAX_SHOTS), content,
                       ShotPlan, budget, job_id, "director")


def validate_plan(plan, steps, primary, devices):
    """Deterministic rules the Director's plan must satisfy before any spend."""
    step_ids = [s["claim_id"] for s in steps]
    placed = [c for shot in plan.shots for c in shot.step_claim_ids] + \
             [n.claim_id for n in plan.not_shown]
    unknown = sorted(set(placed) - set(step_ids))
    if unknown:
        raise PlanRejected(f"plan references unknown claims {unknown}")
    missing = [c for c in step_ids if c not in placed]
    if missing:
        raise PlanRejected(f"plan drops steps {missing}")
    if len(placed) != len(set(placed)):
        raise PlanRejected("a step appears more than once")
    if not plan.shots:
        raise PlanRejected("plan has no shots")
    if len(plan.shots) > MAX_SHOTS:
        raise PlanRejected(f"plan has {len(plan.shots)} shots; limit {MAX_SHOTS}")
    allowed = {primary, *devices}
    for shot in plan.shots:
        if shot.device_product_dir not in allowed:
            raise PlanRejected(f"shot uses product {shot.device_product_dir} not in the question")
        photos = {p["photo_id"]: p for p in official_photos(shot.device_product_dir)}
        if shot.photo_id not in photos:
            raise PlanRejected(f"{shot.photo_id} is not an official photo of {shot.device_product_dir}")
        width, height = photo_size(photos[shot.photo_id]["path"])
        x0, y0, x1, y1 = (shot.crop if len(shot.crop) == 4 else (0, 0, 0, 0)) if shot.crop \
            else (0, 0, width, height)
        if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height) \
                or (x1 - x0) < 128 or (y1 - y0) < 72:
            raise PlanRejected(f"crop {shot.crop} is outside {width}x{height} or too small")
        ratio = (x1 - x0) / (y1 - y0)
        if not CROP_ASPECT[0] <= ratio <= CROP_ASPECT[1]:
            raise PlanRejected(f"shot {shot.photo_id} frame ratio {ratio:.2f}:1 is not close to "
                               f"16:9 (allowed {CROP_ASPECT[0]}-{CROP_ASPECT[1]})")
    return plan


PREFLIGHT_SYSTEM = """\
You check a video shot plan BEFORE any money is spent generating it. Each shot will
animate exactly the starting frame shown to you, so judge that frame, not the whole
photo. A shot fails if the part its step acts on is not clearly visible in the frame
at the location the manual shows, if the frame shows the wrong state for its strategy,
or if the described motion contradicts the manual. Be strict: generating a bad shot
costs about a dollar. Approve only a plan you expect to pass final review.
"""


def preflight_plan(client, budget, job_id, question, steps, plan, product_dir):
    """Cheap check of the exact starting frames before any generation spend."""
    by_id = {s["claim_id"]: s for s in steps}
    content = [{"type": "text", "text": f"Customer question: {question}"}]
    content.extend(manual_blocks(product_dir, steps))
    for i, shot in enumerate(plan.shots, start=1):
        photo = next(p for p in official_photos(shot.device_product_dir)
                     if p["photo_id"] == shot.photo_id)
        content.append({"type": "text", "text": (
            f"Shot {i} — steps: " + "; ".join(by_id[c]["text"] for c in shot.step_claim_ids)
            + f"\nStrategy: {shot.strategy}\nMotion: {shot.motion_prompt}\n"
            + "Must be visible: " + "; ".join(shot.must_be_visible)
            + f"\nExact starting frame ({shot.device_product_dir}, {shot.photo_id}, crop {shot.crop or 'none'}):")})
        content.append(image_block(photo["path"], shot.crop or None, max_side=900))
    return call_claude(client, PREFLIGHT_SYSTEM, content, PlanCheck, budget, job_id, "preflight")


def preflight_problems(check, plan):
    problems = []
    if not check.approve:
        problems.append("preflight did not approve")
    if not check.covers_the_question:
        problems.append("plan does not cover the question")
    for shot_check in check.shots:
        if not (shot_check.part_in_frame and shot_check.state_matches_strategy
                and shot_check.motion_matches_manual):
            problems.append(f"shot {shot_check.shot}: " + ("; ".join(shot_check.issues)
                                                            or "fails a frame check"))
    if len(check.shots) < len(plan.shots):
        problems.append("not every shot was checked")
    return problems


def review_video(client, budget, job_id, question, steps, plan, frames, durations, product_dir):
    by_id = {s["claim_id"]: s for s in steps}
    content = [{"type": "text", "text": (
        f"Customer question: {question}\n\nSteps the video claims to show, in order:\n"
        + "\n".join(f"{c} — {by_id[c]['text']}" for shot in plan.shots
                    for c in shot.step_claim_ids)
        + "\n\nSteps deliberately not shown (text only): "
        + ("; ".join(f"{n.claim_id}: {n.reason}" for n in plan.not_shown) or "none")
        + "\n\nWhat each shot must show:\n"
        + "\n".join(f"Shot {i + 1} ({shot.device_product_dir}, {durations[i]:.1f}s): "
                    + "; ".join(shot.must_be_visible) for i, shot in enumerate(plan.shots)))}]
    content.extend(manual_blocks(product_dir, steps))
    for shot in plan.shots:
        photo = next(p for p in official_photos(shot.device_product_dir)
                     if p["photo_id"] == shot.photo_id)
        content.append({"type": "text", "text": f"Official reference photo for {shot.device_product_dir}:"})
        content.append(image_block(photo["path"], shot.crop or None, max_side=640))
    for seconds, frame in frames:
        content.append({"type": "text", "text": f"Video frame at {seconds:.2f}s:"})
        content.append(image_block(frame, max_side=640))
    return call_claude(client, CRITIC_SYSTEM, content, Critique, budget, job_id, "critic")


def accept(critique, plan):
    """The Critic's verdict, re-checked: every claimed step shown, nothing invented."""
    shown = {v.claim_id for v in critique.steps if v.shown}
    claimed = [c for shot in plan.shots for c in shot.step_claim_ids]
    problems = []
    if critique.verdict != "pass":
        problems.append("critic verdict fail")
    if not critique.answers_the_question:
        problems.append("does not answer the question")
    if not critique.devices_correct:
        problems.append("wrong device")
    if critique.invented_or_wrong:
        problems.append("invented or wrong: " + "; ".join(critique.invented_or_wrong))
    if len(critique.shots) < len(plan.shots):
        problems.append("not every shot has a verdict")
    problems += [f"shot {v.shot} not approved: " + "; ".join(v.issues)
                 for v in critique.shots if not v.approved or v.issues]
    missing = [c for c in claimed if c not in shown]
    if missing:
        problems.append(f"steps not visible: {missing}")
    return problems

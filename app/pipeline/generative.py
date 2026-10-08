"""Automatic generated video for procedures that have no 3D scene.

    Director (Claude) → validate → Executor (FAL Seedance) → Critic (Claude) → publish

The Director (app/pipeline/director.py) decides which devices, official photos,
crops and motions show every step of the customer's question; this module only
executes that plan and enforces money limits. Every paid call - FAL and Claude -
reserves its worst-case price first and is refused past the owner's per-video or
total budget. FAL does not report actual cost, so reservations count as spent.
"""
import json
import datetime as dt
import os
import subprocess
import uuid
from pathlib import Path

from app.pipeline import director
from app.pipeline.store import REPO_ROOT, now
from system import spend_guard

BUDGET_MANIFEST = (REPO_ROOT / "docs" / "workorders" / "approvals" / "manifests"
                   / "video_generation_standing_20260927.json")
GENERATION_SCENE_VERSION = "gen-v3q"     # v3: Claude director + critic; q: 720p quality tier
SEGMENT_SECONDS = 4
TIER = "quality"                        # realism first (owner, 2026-09-27)
RESOLUTION = "720p"
FRAME_SIZE = {"480p": (864, 496), "720p": (1280, 720)}
MAX_ROUNDS = 2                           # generation rounds: first + one re-shoot after review
MAX_PLAN_ATTEMPTS = 3                    # cheap plan attempts per round before any FAL spend
STEADY = (" The camera is completely static. The product keeps its exact shape, colors and "
          "logos. No on-screen text.")

# Worst-case list prices (fal.ai model pages, checked 2026-09-26).
IMAGE_EDIT_USD = 0.15                     # fal-ai/nano-banana-pro/edit, per image
SEEDANCE_USD_PER_SECOND = {               # token-billed; 480p derived from 720p rates
    ("fast", "480p"): 0.12, ("fast", "720p"): 0.2419,
    ("quality", "480p"): 0.15, ("quality", "720p"): 0.3024,
}
VISION_CHECK_USD = 0.01                   # fal-ai/any-llm/vision, one short call


class BudgetExceeded(RuntimeError):
    pass


def price(endpoint, arguments):
    if endpoint.endswith("nano-banana-pro/edit"):
        return IMAGE_EDIT_USD * int(arguments.get("num_images", 1))
    if endpoint.startswith("bytedance/seedance-2.0/"):
        tier = "fast" if "/fast/" in endpoint else "quality"
        rate = SEEDANCE_USD_PER_SECOND[(tier, arguments.get("resolution", "720p"))]
        return rate * float(arguments.get("duration", SEGMENT_SECONDS))
    if endpoint == "fal-ai/any-llm/vision":
        return VISION_CHECK_USD
    raise BudgetExceeded(f"no known price for {endpoint}; refusing the call")


class Budget:
    """The owner's standing video-generation budget, enforced in SQLite."""

    def __init__(self, store):
        self.store = store
        self.config = self._load()

    def _load(self):
        if not BUDGET_MANIFEST.is_file():
            return None
        manifest = json.loads(BUDGET_MANIFEST.read_text())
        digest = spend_guard.manifest_digest(manifest)
        for entry in spend_guard._read_jsonl(spend_guard.DEFAULT_APPROVALS):
            if entry.get("manifest_digest") == digest and entry.get("event") == "approved":
                revoked = any(e.get("event") == "revoked"
                              and e.get("approval_id") == entry["approval_id"]
                              for e in spend_guard._read_jsonl(spend_guard.DEFAULT_APPROVALS))
                if not revoked:
                    per_video = float(manifest["per_video_cap_usd"])
                    if manifest.get("temporary_per_video_until") and dt.datetime.now(dt.timezone.utc) >= dt.datetime.fromisoformat(manifest["temporary_per_video_until"]):
                        per_video = float(manifest["per_video_cap_after_expiry_usd"])
                    return {"approval_id": entry["approval_id"], "run_id": manifest["run_id"],
                            "per_video": per_video,
                            "total": float(manifest["cap_usd"])}
        return None

    def _spent(self, db, job_id=None):
        if job_id:
            row = db.execute("SELECT COALESCE(SUM(amount),0) s FROM spend WHERE job_id=?",
                             (job_id,)).fetchone()
        else:
            row = db.execute("SELECT COALESCE(SUM(amount),0) s FROM spend").fetchone()
        return float(row["s"])

    def remaining(self):
        if not self.config:
            return 0.0
        with self.store.tx() as db:
            return self.config["total"] - self._spent(db)

    def can_start_video(self):
        return bool(self.config) and self.remaining() >= self.config["per_video"] - 1e-9

    @staticmethod
    def providers_ready():
        """Generation needs FAL (video) and Claude (director + critic)."""
        load_provider_key()
        return bool(os.environ.get("FAL_KEY")) and bool(os.environ.get("ANTHROPIC_API_KEY"))

    def reserve(self, job_id, label, amount):
        if not self.config:
            raise BudgetExceeded("no approved video-generation budget")
        with self.store.tx() as db:
            job_spent, total_spent = self._spent(db, job_id), self._spent(db)
            if job_spent + amount > self.config["per_video"] + 1e-9:
                raise BudgetExceeded(f"per-video cap ${self.config['per_video']:.2f} reached")
            if total_spent + amount > self.config["total"] + 1e-9:
                raise BudgetExceeded(f"total budget ${self.config['total']:.2f} reached")
            reservation = "sp_" + uuid.uuid4().hex[:12]
            db.execute("INSERT INTO spend (id, job_id, label, amount, at) VALUES (?,?,?,?,?)",
                       (reservation, job_id, label, amount, now()))
        spend_guard._append_jsonl(spend_guard.DEFAULT_LEDGER, {
            "event": "reserve", "reservation_id": reservation, "at": now(),
            "approval_id": self.config["approval_id"],
            "run_id": self.config["run_id"], "category": "video_generation", "label": label,
            "worst_case_usd": round(amount, 4), "job_id": job_id,
            "note": "counted at worst case until settled"})
        return reservation

    def settle(self, reservation, actual):
        """Replace a worst-case reservation with the provider-reported actual cost."""
        with self.store.tx() as db:
            db.execute("UPDATE spend SET amount=MIN(amount, ?) WHERE id=?", (actual, reservation))
        spend_guard._append_jsonl(spend_guard.DEFAULT_LEDGER, {
            "event": "settle", "at": now(), "reservation_id": reservation,
            "actual_usd": round(actual, 5), "approval_id": (self.config or {}).get("approval_id")})


class MeteredFal:
    """fal_client stand-in: every paid submit is priced and reserved first."""

    def __init__(self, budget, job_id):
        import fal_client
        self._fal = fal_client
        self.budget = budget
        self.job_id = job_id

    def upload_file(self, path):
        return self._fal.upload_file(path)

    def submit(self, endpoint, arguments):
        self.budget.reserve(self.job_id, endpoint, price(endpoint, arguments))
        return self._fal.submit(endpoint, arguments=arguments)


def load_provider_key():
    """FAL_KEY and ANTHROPIC_API_KEY live in the git-ignored .env; load only those."""
    env = REPO_ROOT / ".env"
    if env.is_file():
        for line in env.read_text().splitlines():
            name, _, value = line.partition("=")
            if name in ("FAL_KEY", "ANTHROPIC_API_KEY") and not os.environ.get(name):
                os.environ[name] = value.strip().strip('"')
    try:
        import certifi
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    except ImportError:
        pass
    return bool(os.environ.get("FAL_KEY"))


def stitch(parts, output, work):
    """Concatenate segments at one size and frame rate; returns each duration."""
    import subprocess
    inputs, filters, durations = [], [], []
    for index, (video, _) in enumerate(parts):
        inputs += ["-i", str(video)]
        width, height = FRAME_SIZE[RESOLUTION]
        filters.append(f"[{index}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                       f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:white,fps=24,setsar=1[v{index}]")
        durations.append(float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
             "default=nw=1:nk=1", str(video)], capture_output=True, text=True,
            check=True, timeout=60).stdout.strip()))
    joined = "".join(f"[v{i}]" for i in range(len(parts)))
    graph = ";".join(filters) + f";{joined}concat=n={len(parts)}:v=1:a=0[out]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph,
                    "-map", "[out]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(output)], check=True, timeout=600)
    return durations


def version_for(question, product_dir):
    """Generated videos are specific to the other products the question names."""
    devices = director.mentioned_products(question, product_dir)
    return GENERATION_SCENE_VERSION + "".join(f"+{d}" for d in devices)


def generate(store, job, out_dir, packs_root, steps, product_label, question="",
             resume_dir=None, progress=lambda stage, fraction: None):
    """Plan with the Director, execute on FAL, review with the Critic.

    Shots the Critic approved are kept for later rounds instead of being paid for
    again. `resume_dir` (a previous, interrupted attempt at the same request)
    supplies approved clips and an unreviewed plan to continue from.
    Returns (video, poster, chapters, provenance). Raises if no plan passes.
    """
    budget = Budget(store)
    if not load_provider_key():
        raise RuntimeError("FAL_KEY is not configured")
    client = director.claude_client()
    fal = MeteredFal(budget, job["id"])
    devices = [d for d in job["scene_version"].split("+")[1:] if d]
    product = {"dir": job["product_dir"], "name": product_label}
    provenance = {"rounds": [], "resumed_from": str(resume_dir) if resume_dir else None}
    quality = f"{TIER}-{RESOLUTION}"
    approved = store.library_shots(job["product_dir"], job["procedure_id"], quality)
    resumed, pending_plan, critique = resume_state(resume_dir)
    approved.update(resumed)
    for round_no in range(1, MAX_ROUNDS + 1):
        round_dir = out_dir / f"round-{round_no}"
        round_dir.mkdir(parents=True, exist_ok=True)
        plan = None
        if pending_plan is not None:
            plan, usage = pending_plan, {"reused": "unreviewed plan from the interrupted attempt"}
            pending_plan = None
        record = {"round": round_no, "plan_attempts": []}
        provenance["rounds"].append(record)
        cleared = {}            # shots that passed preflight this round: locked for re-plans
        # Cheapest first: plan, validate and preflight-check the exact starting frames
        # until a plan is approved. No generation money is spent on an unchecked plan.
        for attempt in range(1, MAX_PLAN_ATTEMPTS + 1):
            if plan is None:
                progress("planning" if critique is None else "replanning", 0.05)
                plan, usage = director.plan_shots(client, budget, job["id"], question, product,
                                                  steps, devices, critique,
                                                  approved=[a["shot"] for a in approved.values()])
            # Approved shots are locked: same frame, same motion, same clip.
            locked = {**cleared, **{k: v["shot"] for k, v in approved.items()}}
            plan.shots = [director.Shot(**locked[frozenset(shot.step_claim_ids)])
                          if frozenset(shot.step_claim_ids) in locked else shot
                          for shot in plan.shots]
            entry = {"plan": plan.model_dump(), "director": usage}
            record["plan_attempts"].append(entry)
            try:
                director.validate_plan(plan, steps, job["product_dir"], devices)
                # Shots already proven by final review are not re-judged from their text.
                unproven = [i for i, shot in enumerate(plan.shots)
                            if frozenset(shot.step_claim_ids) not in approved]
                issues, fix = [], ""
                if unproven:
                    progress("checking the plan", 0.08)
                    subset = director.ShotPlan(devices_involved=plan.devices_involved,
                                               shots=[plan.shots[i] for i in unproven],
                                               not_shown=plan.not_shown, notes=plan.notes)
                    check, check_usage = director.preflight_plan(client, budget, job["id"],
                                                                 question, steps, subset,
                                                                 job["product_dir"])
                    entry.update(preflight=check.model_dump(), preflight_usage=check_usage,
                                 preflight_shots=[i + 1 for i in unproven])
                    issues = director.preflight_problems(check, subset)
                    fix = check.fix_notes
                    for shot_check in check.shots:
                        if (shot_check.part_in_frame and shot_check.state_matches_strategy
                                and shot_check.motion_matches_manual
                                and 1 <= shot_check.shot <= len(unproven)):
                            passed = plan.shots[unproven[shot_check.shot - 1]]
                            cleared[frozenset(passed.step_claim_ids)] = passed.model_dump()
            except director.PlanRejected as exc:
                issues, fix = [str(exc)], f"Plan rejected by validation: {exc}"
            entry["issues"] = issues
            save_record(round_dir, record)
            if not issues:
                break
            critique = director.Critique(answers_the_question=False, steps=[],
                                         devices_correct=False, invented_or_wrong=issues,
                                         verdict="fail", fix_notes=fix)
            plan = None
        if plan is None:
            record["rejected"] = "no plan passed the preflight check"
            save_record(round_dir, record)
            break
        record["plan"] = plan.model_dump()
        clips, reused = [], []
        for i, shot in enumerate(plan.shots):
            shot_dir = round_dir / f"shot-{i + 1}"
            keep = (approved.get(frozenset(shot.step_claim_ids)) or {}).get("clip")
            if keep and Path(keep).is_file():
                shot_dir.mkdir(parents=True, exist_ok=True)
                clip = shot_dir / "clip.mp4"
                clip.write_bytes(Path(keep).read_bytes())
                reused.append(i + 1)
            else:
                progress(f"generating clip {i + 1} of {len(plan.shots)}",
                         0.1 + 0.6 * i / len(plan.shots))
                clip = execute_shot(store, shot_dir, fal, shot)
            clips.append(clip)
        record["reused_approved_shots"] = reused
        video = round_dir / "video.mp4"
        durations = stitch([(clip, shot.step_claim_ids) for clip, shot in zip(clips, plan.shots)],
                           video, round_dir)
        progress("reviewing the video", 0.8)
        frames = review_frames(video, round_dir / "review-frames")
        critique, usage = director.review_video(client, budget, job["id"], question, steps,
                                                plan, frames, durations, job["product_dir"])
        problems = director.accept(critique, plan)
        record.update(critic=usage, critique=critique.model_dump(), problems=problems)
        save_record(round_dir, record)
        evict_rejected(store, plan, critique)
        newly = approved_shots(plan, critique, clips)
        for key, item in newly.items():
            if key in approved:
                continue
            store.add_library_shot(job["product_dir"], job["procedure_id"], sorted(key),
                                   item["shot"]["device_product_dir"], quality, item["clip"],
                                   item["shot"], json.dumps([v.model_dump() for v in critique.steps
                                                             if v.claim_id in key]), job["id"])
        approved.update(newly)
        if not problems:
            final = out_dir / "video.mp4"
            final.write_bytes(video.read_bytes())
            poster = out_dir / "poster.jpg"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1", "-i",
                            str(final), "-frames:v", "1", str(poster)], check=True, timeout=60)
            chapters, elapsed = {}, 0.0
            for shot, seconds in zip(plan.shots, durations):
                for claim_id in shot.step_claim_ids:
                    chapters[claim_id] = round(elapsed, 2)
                elapsed += seconds
            by_id = {s["claim_id"]: s["text"] for s in steps}
            provenance["not_shown"] = [f"{by_id[n.claim_id]} ({n.reason})" for n in plan.not_shown]
            provenance["devices"] = devices
            return final, poster, chapters, provenance
    last = provenance["rounds"][-1]
    reason = last.get("rejected") or "; ".join(last.get("problems", []))
    raise RuntimeError(f"no plan passed review: {reason}"[:500])


def save_record(round_dir, record):
    (round_dir / "record.json").write_text(json.dumps(record, indent=1, default=str))


def approved_shots(plan, critique, clips):
    """Shots the Critic approved individually (step visible AND no issue in that shot).

    Seeing the step is not enough: a shot that shows the step but invents a part is
    not approved, so it is regenerated instead of being re-reviewed unchanged.
    """
    shown = {v.claim_id for v in critique.steps if v.shown}
    verdicts = {v.shot: v for v in critique.shots}
    approved = {}
    for index, (shot, clip) in enumerate(zip(plan.shots, clips), start=1):
        verdict = verdicts.get(index)
        if (verdict and verdict.approved and not verdict.issues and shot.step_claim_ids
                and set(shot.step_claim_ids) <= shown):
            approved[frozenset(shot.step_claim_ids)] = {"clip": str(clip), "shot": shot.model_dump()}
    return approved


def resume_state(resume_dirs):
    """(approved clips, unreviewed plan, last critique) from earlier attempts, oldest first."""
    approved, pending, critique = {}, None, None
    if isinstance(resume_dirs, (str, Path)):
        resume_dirs = [resume_dirs]
    round_dirs = [r for d in (resume_dirs or []) if Path(d).is_dir()
                  for r in sorted(Path(d).glob("round-*"), key=lambda p: int(p.name[6:]))]
    for round_dir in round_dirs:
        path = round_dir / "record.json"
        if not path.is_file():
            continue
        record = json.loads(path.read_text())
        if "plan" not in record:
            # A round rejected at preflight: its last attempt's plan was never generated.
            continue
        plan = director.ShotPlan(**record["plan"])
        if record.get("critique"):
            critique = director.Critique(**record["critique"])
            clips = [round_dir / f"shot-{i + 1}" / "clip.mp4" for i in range(len(plan.shots))]
            approved.update(approved_shots(plan, critique, clips))
            pending = None
        elif not record.get("rejected"):
            pending = plan          # planned (and maybe partly generated), never reviewed
    return approved, pending, critique


def shot_cache_key(shot):
    import hashlib
    return hashlib.sha256(json.dumps([shot.device_product_dir, shot.photo_id, shot.crop,
                                      shot.strategy, shot.motion_prompt, TIER, RESOLUTION,
                                      SEGMENT_SECONDS]).encode()).hexdigest()[:20]


def evict_rejected(store, plan, critique):
    """A clip the Critic did not approve must never come back from the cache."""
    import shutil
    verdicts = {v.shot: v for v in critique.shots}
    for index, shot in enumerate(plan.shots, start=1):
        verdict = verdicts.get(index)
        if not verdict or not verdict.approved or verdict.issues:
            shutil.rmtree(store.root / "segments" / shot_cache_key(shot), ignore_errors=True)


def execute_shot(store, shot_dir, fal, shot):
    """One shot: official photo (cropped) → Seedance clip, reversed if needed. Cached."""
    import hashlib
    import shutil
    from PIL import Image
    from app.keyframe_video import DEFAULT_SEED, SEEDANCE_ENDPOINTS, _download
    cache = store.root / "segments" / shot_cache_key(shot)
    shot_dir.mkdir(parents=True, exist_ok=True)
    clip = shot_dir / "clip.mp4"
    if (cache / "clip.mp4").is_file():
        shutil.copy(cache / "clip.mp4", clip)
        return clip
    photo = next(p for p in director.official_photos(shot.device_product_dir)
                 if p["photo_id"] == shot.photo_id)
    image = Image.open(photo["path"]).convert("RGBA")
    flat = Image.new("RGB", image.size, "white")
    flat.paste(image, mask=image.split()[3])
    if shot.crop:
        flat = flat.crop(tuple(shot.crop))
    start = shot_dir / "official.png"
    flat.save(start)
    handle = fal.submit(SEEDANCE_ENDPOINTS[TIER], {
        "prompt": shot.motion_prompt.rstrip() + STEADY, "image_url": fal.upload_file(str(start)),
        "resolution": RESOLUTION, "duration": str(SEGMENT_SECONDS), "aspect_ratio": "16:9",
        "generate_audio": False, "seed": DEFAULT_SEED})
    raw = shot_dir / "raw.mp4"
    _download(handle.get()["video"]["url"], raw)
    reverse = ["-vf", "reverse"] if shot.strategy == "reverse_from_after_photo" else []
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), *reverse, "-an",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(clip)], check=True, timeout=300)
    cache.mkdir(parents=True, exist_ok=True)
    shutil.copy(clip, cache / "clip.mp4")
    return clip


def review_frames(video, out_dir):
    """(seconds, path) pairs spread evenly over the whole video for the Critic."""
    out_dir.mkdir(parents=True, exist_ok=True)
    duration = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
         "default=nw=1:nk=1", str(video)], capture_output=True, text=True, check=True,
        timeout=60).stdout.strip())
    frames = []
    for i in range(director.CRITIC_FRAMES):
        seconds = duration * (i + 0.5) / director.CRITIC_FRAMES
        path = out_dir / f"frame-{i:02d}.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{seconds:.3f}", "-i",
                        str(video), "-frames:v", "1", "-q:v", "3", str(path)],
                       check=True, timeout=60)
        frames.append((seconds, path))
    return frames

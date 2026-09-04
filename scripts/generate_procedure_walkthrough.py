#!/usr/bin/env python3
"""Render any documented procedure into a deterministic walkthrough video.

Unlike the hand-crafted per-procedure scripts, this renderer is generic: it
takes the extracted step claims for one procedure and lays them out as an
animated, typographic walkthrough. Every word shown comes from the step
claims passed in; no product UI or imagery is depicted.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from generate_bluetooth_pairing_video import (  # noqa: E402
    FPS, HEIGHT, WIDTH, FONTS, font, mix, pill, text,
)

INTRO_SECONDS = 3.0
STEP_SECONDS = 3.5
MAX_STEPS = 12

INK = "#17251f"
MUTED = "#5c6a62"
PAPER = "#f6f4ec"
CARD_LINE = "#d7ddd8"
GREEN = "#176744"
GREEN_PALE = "#e6f2eb"
AMBER_PALE = "#fff0c9"

STEP_FONT = font(34, True)
TITLE_FONT = font(56, True)


def readable(value):
    return str(value or "").replace("_", " ").strip().capitalize()


def wrap_text(draw, value, style_font, max_width):
    words = str(value).split()
    lines, line = [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if not line or draw.textlength(candidate, font=style_font) <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def provenance_tag(draw):
    pill(draw, (24, 18, 560, 52), "#17171a", radius=17)
    text(draw, (43, 35), "GENERATED WALKTHROUGH · PENDING OWNER REVIEW",
         "tiny", "#ffffff", "lm")


def intro_frame(frame, t, product_label, procedure, step_count):
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=PAPER)
    draw.ellipse((980, -180, 1460, 300), fill=AMBER_PALE)
    draw.ellipse((-220, 460, 340, 980), fill=GREEN_PALE)
    pill(draw, (92, 104, 1188, 580), "#ffffff", CARD_LINE, 34, 2)
    label = str(product_label or "").upper() or "PRODUCT"
    chip_width = draw.textlength(label, font=FONTS["small"]) + 46
    pill(draw, (132, 145, 132 + chip_width, 183), GREEN_PALE, radius=19)
    text(draw, (132 + chip_width / 2, 164), label, "small", GREEN, "mm")
    y = 245
    for line in wrap_text(draw, readable(procedure), TITLE_FONT, 940)[:3]:
        draw.text((132, y), line, font=TITLE_FONT, fill=INK)
        y += 72
    text(draw, (132, y + 18),
         f"A {step_count}-step generated walkthrough", "body", MUTED)
    text(draw, (132, y + 53),
         "grounded in the captured manual.", "body_bold", MUTED)
    pulse = 8 + int(5 * (1 + math.sin(t * math.pi * 2)))
    draw.ellipse((1080 - pulse, 500 - pulse, 1080 + pulse, 500 + pulse),
                 fill=GREEN)
    provenance_tag(draw)


def step_frame(frame, t, index, steps, product_label):
    step = steps[index]
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#f0f4f0")
    pill(draw, (110, 92, 1170, 560), "#ffffff", CARD_LINE, 28, 2)
    eyebrow = f"{str(product_label or '').upper()} · STEP {step['step_number']}"
    text(draw, (176, 148), eyebrow, "small", GREEN, "lm")

    radius = int(mix(34, 46, min(1.0, t / 0.5)))
    cx, cy = 232, 300
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius),
                 fill=GREEN)
    text(draw, (cx, cy), str(step["step_number"]), "hero", "white", "mm")

    slide = mix(26, 0, min(1.0, t / 0.6))
    y = 240
    for line in wrap_text(draw, step.get("action") or "", STEP_FONT, 760)[:5]:
        draw.text((330 + slide, y), line, font=STEP_FONT, fill=INK)
        y += 52

    total = len(steps)
    text(draw, (176, 508), f"Step {index + 1} of {total}", "small", MUTED, "lm")
    for dot in range(total):
        dx = 1104 - (total - 1 - dot) * 34
        color = GREEN if dot <= index else "#d8ded9"
        draw.ellipse((dx - 8, 500 - 8, dx + 8, 500 + 8), fill=color)

    progress = (index + min(1.0, t / STEP_SECONDS)) / total
    pill(draw, (110, 596, 1170, 614), "#e2e7e2", radius=9)
    pill(draw, (110, 596, 110 + int(1060 * progress), 614), GREEN, radius=9)
    provenance_tag(draw)


def normalized_steps(steps):
    cleaned = []
    for step in steps:
        action = str(step.get("action") or "").strip()
        if not action:
            continue
        cleaned.append({
            "step_number": step.get("step_number") or len(cleaned) + 1,
            "action": action,
        })
    cleaned.sort(key=lambda item: item["step_number"])
    return cleaned[:MAX_STEPS]


def generate(product_label, procedure, steps, output, poster):
    steps = normalized_steps(steps)
    if not steps:
        raise ValueError("At least one step with action text is required")
    output, poster = Path(output), Path(poster)
    output.parent.mkdir(parents=True, exist_ok=True)
    poster.parent.mkdir(parents=True, exist_ok=True)
    duration = INTRO_SECONDS + STEP_SECONDS * len(steps)
    writer = cv2.VideoWriter(
        str(output), cv2.VideoWriter_fourcc(*"avc1"), FPS, (WIDTH, HEIGHT))
    if not writer.isOpened():
        raise RuntimeError("OpenCV could not initialize an H.264 video writer")
    poster_written = False
    poster_at = INTRO_SECONDS + 0.6
    try:
        for frame_index in range(int(FPS * duration)):
            seconds = frame_index / FPS
            frame = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
            if seconds < INTRO_SECONDS:
                intro_frame(frame, seconds, product_label, procedure,
                            len(steps))
            else:
                position = (seconds - INTRO_SECONDS) / STEP_SECONDS
                index = min(int(position), len(steps) - 1)
                step_frame(frame, (position - index) * STEP_SECONDS,
                           index, steps, product_label)
            if not poster_written and seconds >= poster_at:
                frame.save(poster, "PNG")
                poster_written = True
            writer.write(cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR))
    finally:
        writer.release()
    if not output.is_file() or output.stat().st_size < 50_000:
        raise RuntimeError("Generated video is missing or unexpectedly small")
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Render one procedure's steps into a walkthrough video")
    parser.add_argument("--product-label", required=True)
    parser.add_argument("--procedure", required=True)
    parser.add_argument("--steps-json", required=True,
                        help="JSON array of {step_number, action}, or @file")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--poster", type=Path, required=True)
    args = parser.parse_args()
    raw = args.steps_json
    if raw.startswith("@"):
        raw = Path(raw[1:]).read_text(encoding="utf-8")
    generate(args.product_label, args.procedure, json.loads(raw),
             args.output.resolve(), args.poster.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()

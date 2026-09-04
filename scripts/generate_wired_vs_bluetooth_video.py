#!/usr/bin/env python3
"""Generate the mixed wired-vs-Bluetooth connection walkthrough."""

import argparse
import math
from pathlib import Path

import cv2
import numpy as np
from generate_bluetooth_pairing_video import (
    FPS,
    HEIGHT,
    WIDTH,
    cursor,
    font,
    mix,
    pill,
)
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "generated-assets/apple-macbook-air-13-m3/"
    "wired-vs-bluetooth-walkthrough.mp4"
)
DEFAULT_POSTER = (
    ROOT / "generated-assets/apple-macbook-air-13-m3/"
    "wired-vs-bluetooth-walkthrough-poster.png"
)
DURATION = 15
TITLE = font(48, True)
SUBTITLE = font(26, True)
BODY = font(22)
SMALL_BOLD = font(18, True)
TINY = font(14)


def label(draw, xy, value, style=BODY, fill="#1d1d1f", anchor="la"):
    draw.text(xy, value, font=style, fill=fill, anchor=anchor)


def footer(draw, step, caption):
    pill(draw, (24, 18, 512, 52), "#17171a", radius=17)
    label(draw, (43, 35), "GENERATED WALKTHROUGH · CONNECTION ROUTER",
          TINY, "#ffffff", "lm")
    pill(draw, (70, 625, 1210, 690), "#ffffff", "#d7d7dc", 22, 2)
    pill(draw, (91, 643, 135, 675), "#1473e6", radius=16)
    label(draw, (113, 659), str(step), SMALL_BOLD, "white", "mm")
    label(draw, (154, 657), caption, font(23, True), "#1d1d1f", "lm")
    label(draw, (1187, 659), f"{step} / 4", font(17), "#77777d", "rm")


def cable_icon(draw, x, y, color="#176744"):
    draw.line((x - 88, y, x + 28, y), fill=color, width=16)
    pill(draw, (x + 22, y - 27, x + 78, y + 27), color, radius=9)
    draw.rectangle((x + 78, y - 14, x + 100, y + 14), fill=color)
    draw.line((x - 88, y, x - 120, y + 32), fill=color, width=16)
    draw.ellipse((x - 133, y + 20, x - 105, y + 48), fill=color)


def bluetooth_icon(draw, x, y, color="#1473e6"):
    draw.line((x, y - 72, x, y + 72), fill=color, width=13)
    draw.line((x, y - 72, x + 52, y - 20), fill=color, width=13)
    draw.line((x + 52, y - 20, x - 40, y + 54), fill=color, width=13)
    draw.line((x, y + 72, x + 52, y + 20), fill=color, width=13)
    draw.line((x + 52, y + 20, x - 40, y - 54), fill=color, width=13)


def intro(frame, seconds):
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#f4f7fb")
    pill(draw, (92, 96, 1188, 573), "#ffffff", "#d7e1ec", 34, 2)
    label(draw, (132, 171), "“Wired Bluetooth” mixes", TITLE)
    label(draw, (132, 229), "two connection methods.", TITLE)
    pill(draw, (132, 292, 545, 475), "#e8f4ed", radius=25)
    cable_icon(draw, 333, 361)
    label(draw, (338, 438), "WIRED · USE A CABLE", SMALL_BOLD,
          "#176744", "mm")
    pill(draw, (626, 292, 1039, 475), "#e9f2ff", radius=25)
    bluetooth_icon(draw, 833, 367)
    label(draw, (833, 438), "BLUETOOTH · NO CABLE", SMALL_BOLD,
          "#1473e6", "mm")
    draw.line((584, 305, 584, 466), fill="#d6d6dc", width=3)
    footer(draw, 1, "Choose the connection method you actually mean")


def choose_path(frame, seconds):
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#edf3f8")
    label(draw, (640, 111), "Which path matches the device?", SUBTITLE,
          anchor="ma")
    pill(draw, (110, 158, 614, 560), "#ffffff", "#c9d9cf", 28, 2)
    pill(draw, (666, 158, 1170, 560), "#ffffff", "#cbd9ed", 28, 2)
    cable_icon(draw, 362, 271)
    label(draw, (362, 355), "A cable is attached", SUBTITLE,
          "#176744", "ma")
    label(draw, (362, 401), "Use a compatible physical port.", BODY,
          "#5f6762", "ma")
    bluetooth_icon(draw, 918, 272)
    label(draw, (918, 355), "No cable", SUBTITLE, "#1473e6", "ma")
    label(draw, (918, 401), "Use Bluetooth pairing instead.", BODY,
          "#5f6570", "ma")
    footer(draw, 2, "Cable attached? Follow the wired path")


def wired_ports(frame, seconds):
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#e9eef3")
    label(draw, (640, 99), "Wired path: match the connector", SUBTITLE,
          anchor="ma")
    # Laptop deck and side edges.
    draw.polygon(((250, 242), (1016, 242), (1110, 488), (160, 488)),
                 fill="#c4c7cb", outline="#8e9297")
    draw.polygon(((160, 488), (1110, 488), (1064, 524), (210, 524)),
                 fill="#8e9297")
    # Left USB-C/Thunderbolt ports.
    for x in (278, 345):
        pill(draw, (x, 487, x + 43, 501), "#34363a", radius=7)
    # Right headphone jack.
    draw.ellipse((1018, 484, 1038, 504), fill="#303237")
    draw.line((302, 470, 302, 385), fill="#1473e6", width=4)
    pill(draw, (124, 329, 518, 391), "#e9f2ff", "#1473e6", 17, 2)
    label(draw, (321, 349), "USB-C / Thunderbolt accessory", SMALL_BOLD,
          "#145fad", "ma")
    label(draw, (321, 375), "Two ports on the left", font(16),
          "#4b6075", "ma")
    draw.line((1028, 471, 1028, 385), fill="#176744", width=4)
    pill(draw, (759, 329, 1152, 391), "#e8f4ed", "#176744", 17, 2)
    label(draw, (955, 349), "3.5 mm headphones / speakers", SMALL_BOLD,
          "#176744", "ma")
    label(draw, (955, 375), "Headphone jack on the right", font(16),
          "#4e6759", "ma")
    pill(draw, (360, 548, 920, 594), "#fff6db", "#c5962e", 18, 1)
    label(draw, (640, 571), "Check the device documentation before plugging in",
          font(17, True), "#755711", "mm")
    footer(draw, 3, "Use the port that matches the cable and device")


def wireless_path(frame, seconds):
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#dfeaf5")
    pill(draw, (142, 84, 1138, 570), "#f8f8f9", "#c4c7cd", 22, 2)
    draw.rectangle((142, 114, 402, 550), fill="#e7e7eb")
    label(draw, (451, 152), "Bluetooth", font(30, True))
    pill(draw, (420, 228, 1082, 345), "#ffffff", "#d5d5da", 15, 1)
    bluetooth_icon(draw, 480, 286, "#50545b")
    label(draw, (562, 275), "ShowMe Headphones", font(23, True),
          anchor="lm")
    label(draw, (562, 309), "Nearby device", font(17), "#77777d", "lm")
    pill(draw, (916, 263, 1046, 311), "#1473e6", radius=24)
    label(draw, (981, 287), "Connect", font(18, True), "white", "mm")
    cx = mix(770, 978, min(1, seconds / 1.2))
    cy = mix(420, 284, min(1, seconds / 1.2))
    cursor(draw, int(cx), int(cy), click=seconds > 1.35)
    label(draw, (451, 407), "If there is no cable, use the Bluetooth pairing flow.",
          BODY, "#555b63")
    label(draw, (451, 449), "Apple menu › System Settings › Bluetooth",
          SMALL_BOLD, "#1473e6")
    pulse = int(6 + 4 * (1 + math.sin(seconds * math.pi * 2)))
    draw.ellipse((1061 - pulse, 284 - pulse, 1061 + pulse, 284 + pulse),
                 outline="#6aa8ef", width=3)
    footer(draw, 4, "No cable? Use the Bluetooth pairing walkthrough")


def make_frame(seconds):
    frame = Image.new("RGB", (WIDTH, HEIGHT), "#f2f2f4")
    if seconds < 3.0:
        intro(frame, seconds)
    elif seconds < 6.0:
        choose_path(frame, seconds - 3.0)
    elif seconds < 11.0:
        wired_ports(frame, seconds - 6.0)
    else:
        wireless_path(frame, seconds - 11.0)
    return frame


def generate(output, poster):
    output.parent.mkdir(parents=True, exist_ok=True)
    poster.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output), cv2.VideoWriter_fourcc(*"avc1"), FPS, (WIDTH, HEIGHT))
    if not writer.isOpened():
        raise RuntimeError("OpenCV could not initialize an H.264 video writer")
    poster_written = False
    try:
        for index in range(FPS * DURATION):
            seconds = index / FPS
            frame = make_frame(seconds)
            if not poster_written and seconds >= 7.2:
                frame.save(poster, "PNG")
                poster_written = True
            writer.write(cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR))
    finally:
        writer.release()
    if not output.is_file() or output.stat().st_size < 100_000:
        raise RuntimeError("Generated video is missing or unexpectedly small")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--poster", type=Path, default=DEFAULT_POSTER)
    args = parser.parse_args()
    generate(args.output.resolve(), args.poster.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()

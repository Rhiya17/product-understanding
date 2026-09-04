#!/usr/bin/env python3
"""Generate the deterministic Mac Bluetooth-pairing walkthrough asset.

The animation is a deliberately illustrative reconstruction of the documented
macOS flow, not a recording of a specific OS release. Facts and ordering come
from Apple's captured Mac User Guide page in the source vault.
"""

import argparse
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "generated-assets/apple-macbook-air-13-m3/"
    "bluetooth-pairing-walkthrough.mp4"
)
DEFAULT_POSTER = (
    ROOT / "generated-assets/apple-macbook-air-13-m3/"
    "bluetooth-pairing-walkthrough-poster.png"
)
WIDTH, HEIGHT, FPS, DURATION = 1280, 720, 30, 16


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/SFNSRounded.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


FONTS = {
    "hero": font(52, True),
    "title": font(30, True),
    "body": font(23),
    "body_bold": font(23, True),
    "small": font(17),
    "tiny": font(14),
    "sidebar": font(19),
    "button": font(18, True),
}


def ease(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def mix(start, end, value):
    return start + (end - start) * ease(value)


def text(draw, xy, value, style="body", fill="#1d1d1f", anchor="la"):
    draw.text(xy, value, font=FONTS[style], fill=fill, anchor=anchor)


def pill(draw, box, fill, outline=None, radius=18, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def cursor(draw, x, y, click=False):
    points = [(x, y), (x + 10, y + 30), (x + 17, y + 21),
              (x + 25, y + 38), (x + 32, y + 34), (x + 24, y + 18),
              (x + 37, y + 17)]
    if click:
        for radius, alpha in ((34, 55), (22, 95)):
            overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            odraw = ImageDraw.Draw(overlay)
            odraw.ellipse((x - radius, y - radius, x + radius, y + radius),
                          fill=(0, 122, 255, alpha))
            draw._image.paste(overlay, (0, 0), overlay)
    draw.polygon(points, fill="white", outline="#161617")


def chrome(draw, step, caption):
    pill(draw, (24, 18, 510, 52), "#17171a", radius=17)
    text(draw, (43, 35), "GENERATED WALKTHROUGH · ILLUSTRATIVE UI",
         "tiny", "#ffffff", "lm")
    pill(draw, (70, 625, 1210, 690), "#ffffff", "#d7d7dc", 22, 2)
    pill(draw, (91, 643, 135, 675), "#007aff", radius=16)
    text(draw, (113, 659), str(step), "small", "white", "mm")
    text(draw, (154, 657), caption, "body_bold", "#1d1d1f", "lm")
    text(draw, (1187, 659), f"{step} / 4", "small", "#77777d", "rm")


def intro(frame, t):
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle((0, 0, WIDTH, HEIGHT), radius=0,
                           fill="#edf6ff")
    for index, color in enumerate(("#70a7ff", "#a57fff", "#66d3c8")):
        x = 180 + index * 385
        y = 88 + (index % 2) * 92
        draw.ellipse((x - 150, y - 150, x + 150, y + 150), fill=color)
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (245, 248, 255, 205))
    frame.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(frame)
    pill(draw, (92, 104, 1188, 568), "#ffffff", "#d9e4f2", 34, 2)
    pill(draw, (132, 145, 302, 183), "#e7f2ff", radius=19)
    text(draw, (217, 164), "MACBOOK AIR", "small", "#0068d9", "mm")
    text(draw, (132, 250), "Pair a Bluetooth device", "hero")
    text(draw, (132, 319), "A 4-step generated walkthrough grounded in",
         "body", "#5c5c63")
    text(draw, (132, 354), "Apple's Mac User Guide.", "body_bold", "#5c5c63")
    pill(draw, (132, 418, 510, 474), "#1d1d1f", radius=28)
    text(draw, (321, 446), "Starts with the accessory", "small", "white", "mm")
    # Simple Bluetooth glyph.
    bx, by = 1050, 329
    draw.line((bx, by - 86, bx, by + 86), fill="#007aff", width=15)
    draw.line((bx, by - 86, bx + 62, by - 25), fill="#007aff", width=15)
    draw.line((bx + 62, by - 25, bx - 45, by + 66), fill="#007aff", width=15)
    draw.line((bx, by + 86, bx + 62, by + 25), fill="#007aff", width=15)
    draw.line((bx + 62, by + 25, bx - 45, by - 66), fill="#007aff", width=15)
    opacity = int(70 + 35 * math.sin(t * math.pi * 2))
    draw.ellipse((bx - 125, by - 125, bx + 125, by + 125),
                 outline=(0, 122, 255, opacity), width=4)


def prep(frame, t):
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#f1f5fb")
    pill(draw, (158, 95, 1122, 580), "#ffffff", "#d9dce2", 32, 2)
    text(draw, (220, 156), "Prepare the device", "title")
    text(draw, (220, 198), "Turn it on and use its own pairing control.",
         "body", "#66666d")
    # Headphones.
    draw.arc((290, 255, 540, 475), 190, 350, fill="#303036", width=28)
    pill(draw, (278, 355, 355, 486), "#36363b", radius=32)
    pill(draw, (478, 355, 555, 486), "#36363b", radius=32)
    draw.ellipse((493, 420, 520, 447), fill="#007aff")
    pulse = 10 + int(10 * (1 + math.sin(t * math.pi * 3)))
    draw.ellipse((506 - pulse, 433 - pulse, 506 + pulse, 433 + pulse),
                 outline="#69aaff", width=3)
    pill(draw, (650, 272, 1015, 450), "#f7f7fa", "#dedee3", 22, 2)
    text(draw, (700, 319), "ShowMe Headphones", "body_bold")
    text(draw, (700, 360), "Pairing mode", "body", "#5b5b63")
    pill(draw, (700, 393, 898, 429), "#dff5e8", radius=18)
    text(draw, (799, 411), "DISCOVERABLE", "small", "#187a46", "mm")
    chrome(draw, 1, "Make the Bluetooth device discoverable")


def desktop_settings(frame, t):
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#7758c7")
    draw.ellipse((-140, 190, 720, 930), fill="#2948a9")
    draw.ellipse((650, -200, 1480, 500), fill="#e285b7")
    draw.rectangle((0, 0, WIDTH, 32), fill="#f5f5f5")
    text(draw, (18, 16), "●", "small", "#1d1d1f", "lm")
    text(draw, (47, 16), "ShowMe", "small", "#1d1d1f", "lm")
    text(draw, (1188, 16), "⌁  Wi-Fi   10:09", "tiny", "#1d1d1f", "rm")
    pill(draw, (10, 37, 310, 374), "#f8f8fa", "#c8c8ce", 16, 1)
    options = ["About This Mac", "System Settings…", "App Store…",
               "Recent Items", "Sleep", "Restart…", "Shut Down…"]
    for i, option in enumerate(options):
        y = 73 + i * 42
        if i == 1:
            pill(draw, (22, y - 17, 298, y + 18), "#007aff", radius=7)
        text(draw, (36, y), option, "small",
             "white" if i == 1 else "#1d1d1f", "lm")
    cx = mix(520, 163, min(1, t / 1.2))
    cy = mix(395, 112, min(1, t / 1.2))
    cursor(draw, int(cx), int(cy), click=t > 1.35)
    chrome(draw, 2, "Open Apple menu › System Settings")


def settings_panel(frame, t, connected=False):
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#dae5f1")
    pill(draw, (115, 66, 1165, 598), "#f7f7f8", "#babac2", 18, 2)
    draw.rectangle((115, 94, 385, 580), fill="#e9e9ed")
    draw.ellipse((136, 79, 149, 92), fill="#ff5f57")
    draw.ellipse((157, 79, 170, 92), fill="#febc2e")
    draw.ellipse((178, 79, 191, 92), fill="#28c840")
    pill(draw, (140, 119, 359, 158), "#ffffff", "#d2d2d7", 10, 1)
    text(draw, (159, 139), "Search", "small", "#8a8a91", "lm")
    entries = ["Wi-Fi", "Bluetooth", "Network", "Notifications",
               "Sound", "Focus", "General", "Appearance"]
    for i, entry in enumerate(entries):
        y = 196 + i * 43
        if entry == "Bluetooth":
            pill(draw, (132, y - 17, 368, y + 19), "#007aff", radius=8)
        icon_color = "white" if entry == "Bluetooth" else "#5f5f66"
        text(draw, (154, y), "●", "tiny", icon_color, "lm")
        text(draw, (181, y), entry, "sidebar",
             "white" if entry == "Bluetooth" else "#25252a", "lm")
    text(draw, (431, 131), "Bluetooth", "title")
    text(draw, (1077, 131), "On", "body_bold", "#1b7d48", "rm")
    pill(draw, (1078, 113, 1133, 143), "#34c759", radius=15)
    draw.ellipse((1110, 116, 1137, 140), fill="white")
    text(draw, (431, 190), "My Devices", "small", "#77777d")
    pill(draw, (417, 208, 1117, 292), "#ffffff", "#dddddf", 13, 1)
    text(draw, (451, 250), "Magic Keyboard", "body_bold", "#333338", "lm")
    text(draw, (1076, 250), "Connected", "small", "#74747b", "rm")
    text(draw, (431, 338), "Nearby Devices", "small", "#77777d")
    pill(draw, (417, 356, 1117, 458), "#ffffff", "#d5d5da", 13, 1)
    # Headphone icon.
    draw.arc((448, 377, 506, 433), 190, 350, fill="#45454b", width=6)
    pill(draw, (444, 406, 461, 439), "#55555b", radius=7)
    pill(draw, (493, 406, 510, 439), "#55555b", radius=7)
    text(draw, (534, 405), "ShowMe Headphones", "body_bold", "#25252a", "lm")
    if connected:
        text(draw, (1076, 405), "Connected", "small", "#1b7d48", "rm")
        text(draw, (534, 436), "Ready to use", "small", "#77777d", "lm")
        draw.ellipse((1087, 397, 1103, 413), fill="#34c759")
    else:
        pill(draw, (965, 384, 1087, 430), "#007aff", radius=23)
        text(draw, (1026, 407), "Connect", "button", "white", "mm")
        cx = mix(705, 1022, min(1, t / 1.3))
        cy = mix(500, 404, min(1, t / 1.3))
        cursor(draw, int(cx), int(cy), click=t > 1.45)
    if connected:
        chrome(draw, 4, "Connected — accept or enter a code if prompted")
    else:
        chrome(draw, 3, "Choose the device and click Connect")


def make_frame(seconds):
    frame = Image.new("RGB", (WIDTH, HEIGHT), "#f2f2f4")
    if seconds < 2.4:
        intro(frame, seconds)
    elif seconds < 5.4:
        prep(frame, seconds - 2.4)
    elif seconds < 8.5:
        desktop_settings(frame, seconds - 5.4)
    elif seconds < 12.0:
        settings_panel(frame, seconds - 8.5)
    else:
        settings_panel(frame, seconds - 12.0, connected=True)
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
            if not poster_written and seconds >= 9.0:
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

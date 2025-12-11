#!/usr/bin/env python

import os
import sys
import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def extract_datetime(filename):
    # Format: 2025-12-07T09_14_14Z or 2025-12-11T20:47:52Z
    m = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}[_:]\d{2}[_:]\d{2})Z?", filename)
    if m:
        ts = m.group(1).replace("_", ":")
        try:
            return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
        except:
            pass

    # Format: 2025-12-07T091414
    m2 = re.search(r"(\d{4}-\d{2}-\d{2}T)(\d{6})", filename)
    if m2:
        base, raw = m2.group(1), m2.group(2)
        ts = f"{base}{raw[:2]}:{raw[2:4]}:{raw[4:]}"
        try:
            return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
        except:
            pass

    return None


def create_gif_from_images(input_folder, output_gif, width, duration, skip):
    if not os.path.exists(input_folder):
        print(f"GIF not created: folder does not exist → {input_folder}")
        return None

    files = [f for f in os.listdir(input_folder)
             if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not files:
        print("GIF not created: no images found.")
        return None

    items = [(f, extract_datetime(f)) for f in files]
    items = [(f, dt) for f, dt in items if dt]

    if not items:
        print("GIF not created: no valid timestamps in filenames.")
        return None

    items.sort(key=lambda x: x[1])
    items = items[::max(int(skip), 1)]

    start_dt = items[0][1]
    frames = []

    font = None
    font_paths = [
        "Roboto-Regular.ttf",
        "C:/Windows/Fonts/Roboto-Regular.ttf",
        "DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf"
    ]
    
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, 22)
            print(f"Using font: {font_path}")
            break
        except:
            continue
    
    if font is None:
        print("Warning: All fonts failed, using default (small) font")
        font = ImageFont.load_default()

    for fname, dt in items:
        path = os.path.join(input_folder, fname)
        img = Image.open(path).convert("RGB")

        h = int(img.height * (width / img.width))
        img = img.resize((width, h))

        draw = ImageDraw.Draw(img)
        hours = round((dt - start_dt).total_seconds() / 3600)
        label = f"hours: {hours}"

        draw.text((10, 10), label, fill=(128, 128, 128), font=font)

        frames.append(img)

    out_folder = os.path.join(os.path.dirname(input_folder), "output_gif")
    os.makedirs(out_folder, exist_ok=True)
    out_path = os.path.join(out_folder, output_gif)

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(duration * 1000),
        loop=0
    )

    print(f"GIF created: {out_path}")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: create_gif_from_images.py input_folder output_gif width duration skip")
        sys.exit(1)

    create_gif_from_images(
        sys.argv[1],
        sys.argv[2],
        int(sys.argv[3]),
        float(sys.argv[4]),
        sys.argv[5]
    )

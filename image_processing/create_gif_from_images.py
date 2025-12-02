#!/usr/bin/env python

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import re

def extract_date_time_from_filename(filename):
    # Take the last underscore-separated chunk, drop extension
    datetime_str = filename.split("_")[-1].split(".")[0]

    # Handle compact time like YYYY-MM-DDTHHMMSS or YYYY-MM-DDTHHMMSS.xxx
    m = re.match(r"(\d{4}-\d{2}-\d{2}T)(\d{2})(\d{2})(\d{2})(?:\.(\d+))?", datetime_str)
    if m:
        base = m.group(1)
        hh, mm, ss = m.group(2), m.group(3), m.group(4)
        frac = m.group(5)
        if frac:
            datetime_str = f"{base}{hh}:{mm}:{ss}.{frac}"
        else:
            datetime_str = f"{base}{hh}:{mm}:{ss}"

    # Drop trailing 'Z' if present
    datetime_str = datetime_str.rstrip("Z")

    # We only care about date + hour:minute (ignore seconds and below)
    try:
        date_part, time_part = datetime_str.split("T")
        # drop fractional part if any: HH:MM:SS(.fff) -> HH:MM:SS
        time_part = time_part.split(".")[0]
        time_parts = time_part.split(":")
        if len(time_parts) < 2:
            raise ValueError

        hh, mm = time_parts[0], time_parts[1]
        truncated = f"{date_part}T{hh}:{mm}"   # e.g. 2025-12-02T15:51

        return datetime.strptime(truncated, "%Y-%m-%dT%H:%M")
    except Exception:
        print(f"Warning: time data '{datetime_str}' does not match expected format, using now()")
        return datetime.now()

def create_gif_from_images(input_folder, output_gif, width, duration, skip):
    try:
        if not os.path.exists(input_folder):
            print(f"Error: The input folder '{input_folder}' does not exist.")
            return

        image_files = [
            f for f in os.listdir(input_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]

        if not image_files:
            print("No image files found in the folder.")
            return

        image_files.sort()

        # validate skip
        try:
            skip_n = int(skip)
        except ValueError:
            print(f"Invalid skip value '{skip}', defaulting to 1")
            skip_n = 1

        if skip_n <= 0:
            print(f"Non-positive skip value '{skip_n}', defaulting to 1")
            skip_n = 1

        image_counter = 0
        start_datetime = None
        images = []

        for image_file in image_files:
            image_counter += 1

            if image_counter % skip_n != 0:
                continue

            image_path = os.path.join(input_folder, image_file)
            img = Image.open(image_path)

            # Resize proportionally
            height = int(img.height * (width / img.width))
            img_resized = img.resize((width, height))

            current_datetime = extract_date_time_from_filename(image_file)

            if start_datetime is None:
                start_datetime = current_datetime
                hours_passed = 0
            else:
                hours_passed = int((current_datetime - start_datetime).total_seconds() / 3600)

            draw = ImageDraw.Draw(img_resized)
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 20)
            except Exception:
                font = ImageFont.load_default()

            draw.text((10, 10), f"{hours_passed} hours", fill=(255, 255, 255), font=font)
            images.append(img_resized)

        if not images:
            print("No frames selected after applying skip. GIF not created.")
            return

        input_parent_folder = os.path.dirname(input_folder)
        output_folder = os.path.join(input_parent_folder, "..", "output_gif_folder")
        os.makedirs(output_folder, exist_ok=True)

        output_gif_path = os.path.join(output_folder, output_gif)
        images[0].save(
            output_gif_path,
            save_all=True,
            append_images=images[1:],
            duration=int(duration * 1000),
            loop=0
        )

        print(f"GIF created and saved as {output_gif_path} with a duration of {duration} seconds.")
        return output_gif_path

    except Exception as e:
        import traceback
        print("An error occurred:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: create_gif_from_images.py input_folder output_gif width duration skip")
    else:
        input_folder = sys.argv[1]
        output_gif = sys.argv[2]
        width = int(sys.argv[3])
        duration = float(sys.argv[4])
        skip = sys.argv[5]
        create_gif_from_images(input_folder, output_gif, width, duration, skip)

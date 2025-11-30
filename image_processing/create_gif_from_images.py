#!/usr/bin/env python

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import re

def extract_date_time_from_filename(filename):
    # match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}\.\d+", filename)
    # if not match:
    #     raise ValueError("No timestamp found")
    # return datetime.strptime(match.group(0).replace('_', ':'), "%Y-%m-%dT%H:%M:%S.%f")
    datetime_str = filename.split("_")[-1].split(".")[0]

    # If datetime_str looks like YYYY-MM-DDTHHMMSS (no colons), insert colons for parsing
    # e.g. 2025-11-29T214924 -> 2025-11-29T21:49:24
    m = re.match(r"(\d{4}-\d{2}-\d{2}T)(\d{2})(\d{2})(\d{2})(?:\.(\d+))?", datetime_str)
    if m:
        base = m.group(1)
        hh, mm, ss = m.group(2), m.group(3), m.group(4)
        frac = m.group(5)
        if frac:
            datetime_str = f"{base}{hh}:{mm}:{ss}.{frac}"
        else:
            datetime_str = f"{base}{hh}:{mm}:{ss}"

    # Attempt parsing with and without fractional seconds
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue

    print(f"Error: time data '{datetime_str}' does not match expected format")
    return datetime.now()

def create_gif_from_images(input_folder, output_gif, width, duration, skip):
    try:
        # Check if the input folder exists
        if not os.path.exists(input_folder):
            print(f"Error: The input folder '{input_folder}' does not exist.")
            return

        # List all image files in the folder
        image_files = [f for f in os.listdir(input_folder) if f.endswith((".png", ".jpg", ".jpeg", ".gif"))]

        if not image_files:
            print("No image files found in the folder.")
            return

        # Sort image files by name to maintain order
        image_files.sort()

        # Initialize a counter to keep track of the images
        image_counter = 0
        start_datetime = None  # Initialize the start datetime

        images = []
        for image_file in image_files:
            # Increment the counter for each image
            image_counter += 1

            # Skip every nth image based on the provided parameter
            if image_counter % int(skip) != 0:
                continue

            image_path = os.path.join(input_folder, image_file)
            img = Image.open(image_path)

            # Calculate the proportional height based on the desired width
            height = int(img.height * (width / img.width))

            # Resize the image to the desired width and proportional height
            img_resized = img.resize((width, height))

            # Extract the date and time using the new function
            current_datetime = extract_date_time_from_filename(image_file)

            # Calculate the number of hours passed since the start datetime
            if start_datetime is None:
                start_datetime = current_datetime
                hours_passed = 0
            else:
                hours_passed = int((current_datetime - start_datetime).total_seconds() / 3600)

            # Create a drawing context and font (fall back to default if DejaVu not available)
            draw = ImageDraw.Draw(img_resized)
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 20)
            except Exception:
                font = ImageFont.load_default()
            # Position and text color for the hours annotation
            position = (10, 10)
            text_color = (255, 255, 255)

            # Add the current hour as text to the image
            draw.text(position, f"{hours_passed} hours", fill=text_color, font=font)

            images.append(img_resized)

        # Construct the output folder path two levels above the input folder
        input_parent_folder = os.path.dirname(input_folder)
        output_folder = os.path.join(input_parent_folder, "..", "output_gif_folder")

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Save the images as a GIF in the output folder with the specified duration
        output_gif_path = os.path.join(output_folder, output_gif)
        images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=int(duration * 1000), loop=0)

        print(f"GIF created and saved as {output_gif_path} with a duration of {duration} seconds.")

        # return the full path to the created GIF so callers can upload or further process it
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

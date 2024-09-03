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
   def extract_date_time_from_filename(filename):
    try:
        datetime_str = filename.split("_")[-1].split(".")[0]
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f")
    except Exception as e:
        print(f"Error: {e}")
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

            # Create a drawing context and font
            draw = ImageDraw.Draw(img_resized)
            font = ImageFont.truetype("DejaVuSans.ttf", 20)  # Ensure the font is available on your system
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
    except Exception as e:
        print(f"An error occurred: {str(e)}")

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

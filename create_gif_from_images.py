#!/usr/bin/env python

import os
import sys
from PIL import Image

def create_gif_from_images(input_folder, output_gif, duration, skip):
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

        images = []
        for image_file in image_files:
            # Increment the counter for each image
            image_counter += 1

            # Skip every nth image based on the provided parameter
            if image_counter % int(skip) != 0:
                continue

            image_path = os.path.join(input_folder, image_file)
            img = Image.open(image_path)
            images.append(img)

        # Construct the output folder path two levels above the input folder
        input_parent_folder = os.path.dirname(input_folder)
        output_folder = os.path.join(input_parent_folder, "..", "output_gif_folder")

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Save the images as a GIF in the output folder with the specified duration
        output_gif_path = os.path.join(output_folder, output_gif)
        images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=int(duration) * 100, loop=0)

        print(f"GIF created and saved as {output_gif_path} with a duration of {duration} seconds.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: create_gif_from_images.py input_folder output_gif duration skip")
    else:
        input_folder = sys.argv[1]
        output_gif = sys.argv[2]
        duration = float(sys.argv[3])
        skip = sys.argv[4]
        create_gif_from_images(input_folder, output_gif, duration, skip)

#!/usr/bin/env python

import os
import sys
from PIL import Image, ImageSequence

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) != 3:
    print("Usage: create_gif_from_images.py output_gif duration")
    sys.exit(1)

output_gif = sys.argv[1]
duration = int(float(sys.argv[2]) * 100)  # Duration in centiseconds

input_folder = os.path.join(script_dir, "captured_images/B")  # Path to the input folder

# List all image files in the folder
image_files = [f for f in os.listdir(input_folder) if f.endswith((".png", ".jpg", ".jpeg", ".gif"))]

if not image_files:
    print("No image files found in the folder.")
    sys.exit(1)

# Sort image files by name to maintain order
image_files.sort()

images = []
for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    img = Image.open(image_path)
    images.append(img)

# Create a directory for GIF files if it doesn't exist
gif_folder = os.path.join(script_dir, "gif_files")
os.makedirs(gif_folder, exist_ok=True)

# Save the images as a GIF in the GIF folder with the specified duration
output_gif_path = os.path.join(gif_folder, output_gif)
images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=duration, loop=0)

print(f"GIF created and saved as {output_gif_path} with a duration of {duration} centiseconds.")

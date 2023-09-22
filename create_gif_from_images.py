#!/usr/bin/env python

import os
import sys
import imageio
from PIL import Image

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) != 2:
    print("Usage: create_gif_from_images.py output_gif")
    sys.exit(1)

output_gif = sys.argv[1]
input_folder = os.path.join(script_dir, "captured_images/A")  # Path to the input folder

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

# Save the images as a GIF in the GIF folder
output_gif_path = os.path.join(gif_folder, output_gif)
imageio.mimsave(output_gif_path, images, duration=0.2)  # Adjust the duration as needed

print(f"GIF created and saved as {output_gif_path}")

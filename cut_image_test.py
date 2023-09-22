import os
from cut_and_save_rectangle import cut_and_save_rectangle

# Define the folder containing captured images
captured_images_folder = "captured_images"

# Define the coordinates for cropping
x = 300
y = 890
width = 475
height = 600
output_directory = "C"  # Set output directory to "C"

# Iterate through the files in the captured_images folder
try:
    for filename in os.listdir(captured_images_folder):
        if filename.endswith(".jpg"):
            # Construct the full path to the image file
            image_file_path = os.path.join(captured_images_folder, filename)
            
            # Call the cut_and_save_rectangle function for each image
            cut_and_save_rectangle(image_file_path, x, y, width, height, output_directory)
except Exception as e:
    print(f"Error: {e}")

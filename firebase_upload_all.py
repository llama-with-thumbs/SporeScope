import os
from firebase_uploader import upload_image_to_firebase

# Define the list of directories (A, B, C) to process
directories = ["A", "B", "C"]

# Iterate through the specified directories
for directory in directories:
    # Construct the path to the directory inside captured_images
    current_directory = os.path.join("captured_images", directory)

    # Check if the directory exists
    if os.path.exists(current_directory):
        # Iterate through the files in the current directory
        for filename in os.listdir(current_directory):
            if filename.endswith(".jpg"):
                # Construct the full path to the image file
                image_file_path = os.path.join(current_directory, filename)
                
                upload_image_to_firebase(image_file_path, image_file_path)
    else:
        print(f"Directory {directory} does not exist.")

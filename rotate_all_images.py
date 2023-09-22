import os
from rotate_image import rotate_image

# Define the folder containing captured images
captured_images_folder = "captured_images"

# Define the rotation angle
rotation_angle = -2.5  # Rotation angle in degrees

# Check if the folder exists
if os.path.exists(captured_images_folder) and os.path.isdir(captured_images_folder):
    # Get a list of all files in the folder
    image_files = [f for f in os.listdir(captured_images_folder) if os.path.isfile(os.path.join(captured_images_folder, f))]

    # Iterate over the image files
    for image_file in image_files:
        try:
            # Construct the full path to the image file
            image_file_path = os.path.abspath(os.path.join(captured_images_folder, image_file))

            # Call the rotate_image function for the current image
            rotated_image = rotate_image(image_file_path, rotation_angle)

            # Check if the rotation was successful
            if rotated_image is not None:
                print(f"Rotated and saved: {os.path.join(captured_images_folder, image_file)}")
            else:
                print(f"Image rotation failed for: {os.path.join(captured_images_folder, image_file)}")
        except Exception as e:
            print(f"Error processing {os.path.join(captured_images_folder, image_file)}: {e}")
else:
    print(f"Error: Folder '{captured_images_folder}' does not exist or is not a directory.")

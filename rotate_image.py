import cv2
import os

# Directory containing the images to be rotated
input_directory = 'captured_images'

# Output directory to save the rotated images
output_directory = 'rotated_images'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define the rotation angle in degrees
angle = 2

# List all files in the input directory
file_list = os.listdir(input_directory)

# Process each image file
for filename in file_list:
    if filename.endswith('.jpg'):
        # Construct the full paths for input and output files
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename)

        # Load the image
        image = cv2.imread(input_path)

        if image is not None:
            # Get the image dimensions
            height, width = image.shape[:2]

            # Calculate the rotation matrix
            rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), -angle, 1)

            # Perform the rotation
            rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

            # Save the rotated image
            cv2.imwrite(output_path, rotated_image)

            print(f"Rotated and saved: {output_path}")

print("All images processed.")

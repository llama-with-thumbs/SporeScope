import cv2
import sys
import os

def cut_and_save_rectangle(image_path, x, y, width, height, output_directory):
    try:
        # Load the image
        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError("Image not found or could not be opened.")

        # Crop the rectangle from the image
        cropped_image = image[y:y+height, x:x+width]

        # Get the directory and filename from the input path
        directory, filename = os.path.split(image_path)

        # Construct the output directory path
        output_directory_path = os.path.join(directory, output_directory)

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory_path, exist_ok=True)

        # Construct the output path within the specified directory
        output_path = os.path.join(output_directory_path, "cropped_" + filename)

        # Save the cropped rectangle as a new image in the specified directory
        cv2.imwrite(output_path, cropped_image)
        print(f"Saved cropped image as {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python cut_rectangle.py input_image x y width height output_directory")
    else:
        input_image = sys.argv[1]
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        width = int(sys.argv[4])
        height = int(sys.argv[5])
        output_directory = sys.argv[6]
        cut_and_save_rectangle(input_image, x, y, width, height, output_directory)

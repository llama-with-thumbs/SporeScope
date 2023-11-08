import cv2
import sys
import os

def cut_and_save_snippet(image_path, x, y, width, height, flask, chamber):
    try:
        # Load the image
        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError("Image not found or could not be opened.")

        # Crop the rectangle from the image
        cropped_image = image[y:y+height, x:x+width]

        # Get the filename from the input path
        filename = os.path.basename(image_path)

        # Construct the output directory path
        output_directory_path = os.path.join(chamber, flask)

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory_path, exist_ok=True)

        # Construct the output path within the specified directory
        output_path = os.path.join(output_directory_path, filename)

        # Save the cropped rectangle as a new image in the specified directory
        cv2.imwrite(output_path, cropped_image)
        print(f"Saved cropped image as {output_path}")
        
        # Return the path of the newly created cropped image
        return output_path
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

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
        cropped_image_path = cut_and_save_snippet(input_image, x, y, width, height, output_directory)
        
        if cropped_image_path:
            print(f"Newly created cropped image path: {cropped_image_path}")
        else:
            print("Error occurred during image processing.")

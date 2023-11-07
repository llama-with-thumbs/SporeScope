import cv2
import sys
import os

def draw_red_rectangles(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)

        if image is None:
            print("Error: Unable to load the image.")
            return

        # Define the coordinates and dimensions of the rectangles
        rectangle_coordinates = [
            (410, 868, 425, 530),  # (x, y, width, height) of the first rectangle
            (1060, 868, 425, 530),  # (x, y, width, height) of the second rectangle
            (1700, 868, 425, 530),   # (x, y, width, height) of the third rectangle
        ]

        # Draw red rectangles on the image
        for (x, y, width, height) in rectangle_coordinates:
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), thickness=10)

        # Get the directory and filename of the input image
        input_dir, input_filename = os.path.split(image_path)

        # Create the output image path by adding "_with_rectangles" to the filename
        output_filename = os.path.splitext(input_filename)[0] + "_with_rectangles" + os.path.splitext(input_filename)[1]
        output_path = os.path.join(input_dir, output_filename)

        # Save the image with red rectangles in the same folder
        cv2.imwrite(output_path, image)

        print(f"Red rectangles added and saved to {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}")

def find_first_image_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("No image files found in the folder.")
        return None

    # Sort the image files and select the first one
    image_files.sort()
    first_image = os.path.join(folder_path, image_files[0])
    return first_image

if __name__ == "__main__":
    # Use "test.jpg" in the same folder as the script
    current_folder = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_folder, "test.jpg")
    
    draw_red_rectangles(image_path)
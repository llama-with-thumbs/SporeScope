import cv2
import numpy as np

def calculate_mean_intensities(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)

        if image is None:
            print("Error: Unable to load the image.")
            return None

        # Calculate the mean intensities for each channel (BGR)
        mean_blue = np.mean(image[:, :, 0])  # Blue channel
        mean_green = np.mean(image[:, :, 1])  # Green channel
        mean_red = np.mean(image[:, :, 2])  # Red channel

        # Round the mean intensities to two decimal places
        mean_blue = round(mean_blue, 2)
        mean_green = round(mean_green, 2)
        mean_red = round(mean_red, 2)

        return mean_red, mean_green, mean_blue

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    image_path = "your_image.jpg"  # Replace with the path to your image
    mean_red, mean_green, mean_blue = calculate_mean_intensities(image_path)

    if mean_red is not None:
        print(f"Mean Red Intensity: {mean_red}")
        print(f"Mean Green Intensity: {mean_green}")
        print(f"Mean Blue Intensity: {mean_blue}")

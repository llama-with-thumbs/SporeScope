import cv2
import numpy as np

def calculate_green_object_area(image_path):
    # Load the image from the given path
    image = cv2.imread(image_path)

    # Convert the image to HSV color space to better detect the green color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    # Create a mask for green objects
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Apply minimal Gaussian Blur (using a small kernel size for minimal smoothing)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)

    # Convert the mask to grayscale for contour detection
    gray_mask = mask

    # Find contours in the masked grayscale image
    contours, _ = cv2.findContours(gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Variable to store the total surface area of the object(s)
    total_area = 0

    # Loop through each contour, calculate area
    for contour in contours:
        area = cv2.contourArea(contour)
        total_area += area  # Add the area to the total

    return total_area

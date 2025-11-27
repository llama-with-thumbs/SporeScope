import cv2
import numpy as np

def calculate_green_object_area(image_paths):
    """
    Accepts either a single image path (string) or a list of image paths.
    Returns the area (int) or list of areas.
    """
    
    # Normalize input to list
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    areas = []  # To collect results

    for image_path in image_paths:
        image = cv2.imread(image_path)

        if image is None:
            print(f"⚠ Warning: Could not open image: {image_path}")
            areas.append(None)
            continue

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.GaussianBlur(mask, (3, 3), 0)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        total_area = sum(cv2.contourArea(contour) for contour in contours)
        areas.append(total_area)

    # If the input was a single path, return a single value instead of list
    return areas[0] if len(areas) == 1 else areas

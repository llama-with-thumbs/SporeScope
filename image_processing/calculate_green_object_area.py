import cv2
import numpy as np

def calculate_green_object_area(image_paths):
    """
    Accepts either a single image path (string) or a list of image paths.
    Returns a single area value (int) if one path,
    or a list of area values if multiple paths.
    """
    
    # Normalize to list
    single_input = False
    if isinstance(image_paths, str):
        single_input = True
        image_paths = [image_paths]

    results = []

    for path in image_paths:
        try:
            image = cv2.imread(path)
            if image is None:
                print(f"⚠️ Unable to load image: {path}")
                results.append(None)
                continue

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            lower_green = np.array([35, 100, 100])
            upper_green = np.array([85, 255, 255])

            mask = cv2.inRange(hsv, lower_green, upper_green)
            mask = cv2.GaussianBlur(mask, (3, 3), 0)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            total_area = sum(cv2.contourArea(contour) for contour in contours)

            results.append(total_area)

        except Exception as e:
            print(f"⚠️ Error processing {path}: {str(e)}")
            results.append(None)

    # Return single value instead of list if input was single
    return results[0] if single_input else results

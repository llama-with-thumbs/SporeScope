import cv2

def calculate_contour_areas_mm2(contours, image_height_px=500, image_height_mm=58.0):
    """
    Calculate TOTAL contour area in mm².

    Args:
        contours (list[np.ndarray]): OpenCV contours
        image_height_px (int): image height in pixels
        image_height_mm (float): real image height in mm

    Returns:
        float: total area of all contours in mm²
    """

    if not contours:
        return 0.0

    mm_per_pixel = image_height_mm / image_height_px
    mm2_per_pixel2 = mm_per_pixel ** 2

    total_area = sum(cv2.contourArea(c) * mm2_per_pixel2 for c in contours)
    return round(total_area, 2)

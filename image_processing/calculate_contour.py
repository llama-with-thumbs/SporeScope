import cv2
import numpy as np


def calculate_contour(image_path, min_area=300, safe_radius_ratio=0.87):
    """
    Detect and display dark mycelium blobs on a bright agar plate.
    Filters out detections near edges and corners using a circular mask.
    """

    # Load with alpha channel
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")

    # Split channels
    if img.shape[2] == 4:
        bgr = img[:, :, :3]
        alpha = img[:, :, 3]
        valid_mask = alpha > 0
    else:
        bgr = img
        valid_mask = np.ones(bgr.shape[:2], dtype=bool)

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Mask out transparent pixels
    gray_masked = gray.copy()
    gray_masked[~valid_mask] = 255

    # --- Mild blur ---
    blur = cv2.GaussianBlur(gray_masked, (5, 5), 0)

    # --- Adaptive threshold for DARK objects ---
    binary = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        41,
        5
    )

    binary[~valid_mask] = 0

    # --- Morphological cleanup ---
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    clean = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # --- Find contours ---
    contours, _ = cv2.findContours(
        clean,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # -------------------------------------------------
    # Circular edge/corner suppression
    # -------------------------------------------------
    cx, cy = w // 2, h // 2
    plate_radius = min(cx, cy)
    safe_radius = int(plate_radius * safe_radius_ratio)

    filtered = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        if area > 0.25 * h * w:
            continue

        M = cv2.moments(c)
        if M["m00"] == 0:
            continue

        cx_c = int(M["m10"] / M["m00"])
        cy_c = int(M["m01"] / M["m00"])

        # Distance from image center
        d = np.sqrt((cx_c - cx) ** 2 + (cy_c - cy) ** 2)

        # Reject anything outside safe circle
        if d > safe_radius:
            continue

         

        filtered.append(c)

    # # --- Draw result ---
    # result = bgr.copy()

    # # Optional: visualize safe circle
    # cv2.circle(result, (cx, cy), safe_radius, (255, 0, 0), 1)

    # cv2.drawContours(result, filtered, -1, (0, 255, 0), 2)

    # # --- Display ---
    # cv2.imshow("Detected mycelium (circular edge filtered)", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # ✅ RETURN NUMPY ARRAYS
    return filtered
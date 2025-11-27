import cv2
import os
import numpy as np

def cut_and_save_circle_snippets(image_path, circle_coords_list, plates, chamber):
    """
    image_path: path to image file
    circle_coords_list: list of (cx, cy, r)
    plates: list of plate IDs (same length as circle_coords_list)
    chamber: chamber ID
    """
    try:
        if len(circle_coords_list) != len(plates):
            raise ValueError("circle_coords_list and plates must have the same length.")

        # Load image
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise FileNotFoundError("Image not found or could not be opened.")

        # Ensure image has 4 channels (RGBA/BGRA)
        if image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        filename = os.path.basename(image_path)  # ⬅️ Use original filename (same behavior)
        saved_paths = []

        # Loop plate-by-plate (each plate has matching circle)
        for plate, (cx, cy, r) in zip(plates, circle_coords_list):
            output_directory = os.path.join("captured_images", chamber, plate)
            os.makedirs(output_directory, exist_ok=True)

            # Create mask
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.circle(mask, (cx, cy), r, 255, -1)

            # Apply mask for transparent cutout
            result = np.zeros_like(image)
            result[mask == 255] = image[mask == 255]

            # Crop to bounding square
            x1, y1 = cx - r, cy - r
            x2, y2 = cx + r, cy + r
            cropped = result[y1:y2, x1:x2]

            # Save using original filename (same as rectangle version)
            output_path = os.path.join(output_directory, filename)
            cv2.imwrite(output_path, cropped)
            saved_paths.append(output_path)

            print(f"Saved cropped circular snippet for plate {plate}: {output_path}")

        return saved_paths

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

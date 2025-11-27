import cv2
import sys
import os
import numpy as np

def cut_and_save_circle_snippet(image_path, circle_coords, plate, chamber):
    cx, cy, r = circle_coords  # center_x, center_y, radius

    try:
        # Load image with alpha channel (so transparency works)
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        if image is None:
            raise FileNotFoundError("Image not found or could not be opened.")

        # Create mask (transparent outside the circle)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (cx, cy), r, 255, -1)  # filled circle

        # Convert to 4-channel (RGBA) if not already
        if image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

        # Apply mask — keep circle, make outside transparent
        result = np.zeros_like(image)
        result[mask == 255] = image[mask == 255]

        # Crop tightly around the circle
        x1, y1 = cx - r, cy - r
        x2, y2 = cx + r, cy + r
        cropped = result[y1:y2, x1:x2]

        # Prepare output path
        filename = os.path.basename(image_path)
        base_name, _ = os.path.splitext(filename)  # remove extension
        output_directory_path = os.path.join("captured_images", chamber, plate)
        os.makedirs(output_directory_path, exist_ok=True)

        output_path = os.path.join(output_directory_path, f"{base_name}_circle.png")

        # Save as PNG (to keep transparency)
        cv2.imwrite(output_path, cropped)
        print(f"Saved circular cutout: {output_path}")

        return output_path

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

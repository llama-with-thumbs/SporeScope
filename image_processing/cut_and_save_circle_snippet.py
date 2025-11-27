import cv2
import os
import numpy as np

def cut_and_save_circle_snippets(image_path, circle_coords_list, plates, chamber):
    """
    image_path: path to image file
    circle_coords_list: list of (cx, cy, r)
    plates: list of plate IDs
    chamber: chamber ID
    """
    try:
        # Load image with alpha support
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise FileNotFoundError("Image not found or could not be opened.")

        # Convert to RGBA if needed
        if image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

        base_name = os.path.splitext(os.path.basename(image_path))[0]
        saved_paths = []

        # Loop through each plate
        for plate in plates:
            output_directory = os.path.join("captured_images", chamber, plate)
            os.makedirs(output_directory, exist_ok=True)

            # Loop through each circle for this plate
            for idx, (cx, cy, r) in enumerate(circle_coords_list, start=1):
                # Create mask
                mask = np.zeros(image.shape[:2], dtype=np.uint8)
                cv2.circle(mask, (cx, cy), r, 255, -1)

                # Apply mask using transparency
                result = np.zeros_like(image)
                result[mask == 255] = image[mask == 255]

                # Crop circle tightly
                x1, y1 = cx - r, cy - r
                x2, y2 = cx + r, cy + r
                cropped = result[y1:y2, x1:x2]

                # Save file with ID in name
                output_path = os.path.join(
                    output_directory,
                    f"{base_name}_circle_{idx}.png"
                )
                cv2.imwrite(output_path, cropped)
                saved_paths.append(output_path)

                print(f"Saved: {output_path}")

        return saved_paths

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

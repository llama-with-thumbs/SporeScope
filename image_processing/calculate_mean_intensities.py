import cv2
import numpy as np

def calculate_mean_intensities(image_paths):
    """
    Accepts either a single image path (string) or a list of image paths.
    Returns a single (r, g, b) tuple if one path,
    or a list of (r, g, b) tuples if multiple paths.
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

            mean_blue = round(np.mean(image[:, :, 0]), 2)
            mean_green = round(np.mean(image[:, :, 1]), 2)
            mean_red = round(np.mean(image[:, :, 2]), 2)

            results.append((mean_red, mean_green, mean_blue))

        except Exception as e:
            print(f"⚠️ Error processing {path}: {str(e)}")
            results.append(None)

    # Return single result instead of list if only 1 input
    return results[0] if single_input else results


# Optional quick test
if __name__ == "__main__":
    test_paths = ["img1.png", "img2.png"]
    print(calculate_mean_intensities(test_paths))

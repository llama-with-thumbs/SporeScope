import cv2
import os

def draw_red_rectangle(image_path):
    try:
        print("Using image:", image_path)
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Unable to load image")
            return

        x, y, width, height = 630, 520, 2100, 1450
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 10)

        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_with_rectangle{ext}"

        cv2.imwrite(output_path, image)
        print("Saved:", output_path)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    image_path = "test.jpg"
    draw_red_rectangle(image_path)

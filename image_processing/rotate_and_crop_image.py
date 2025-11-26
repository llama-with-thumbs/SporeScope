import cv2

def rotate_and_crop_image(input_path, angle, raw_coordinates=None):
    try:
        image = cv2.imread(input_path)
        if image is None:
            print("Error: Unable to load image at {}".format(input_path))
            return

        height, width = image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), -angle, 1)
        rotated = cv2.warpAffine(image, rotation_matrix, (width, height))

        if raw_coordinates:
            x, y, w, h = raw_coordinates
            rotated = rotated[y:y + h, x:x + w]

        cv2.imwrite(input_path, rotated)
        print("Processed and saved: {}".format(input_path))

    except Exception as e:
        print("Error: {}".format(e))

import cv2

def rotate_image(input_path, angle=2):
    try:
        # Load the image
        image = cv2.imread(input_path)

        if image is not None:
            # Get the image dimensions
            height, width = image.shape[:2]

            # Calculate the rotation matrix
            rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), -angle, 1)

            # Perform the rotation
            rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

            # Save the rotated image with the same filename, overwriting the original
            cv2.imwrite(input_path, rotated_image)

            print("Rotated and saved: {}".format(input_path))  # Use older string formatting here
        else:
            print("Error: Unable to load image at {}".format(input_path))

    except Exception as e:
        print("Error: {}".format(e))

import cv2

# Set the resolution (width and height)
width, height = 2592, 1944  # Desired resolution

# Set the shutter speed (in microseconds)
shutter_speed = 32955  # 1/30 second exposure time

# Initialize the camera with the specified resolution
camera = cv2.VideoCapture(0)
camera.set(3, width)  # Set the width
camera.set(4, height)  # Set the height

# Set the shutter speed (if supported by the camera)
camera.set(cv2.CAP_PROP_EXPOSURE, shutter_speed)

# Set the white balance (e.g., AWB mode)
camera.set(cv2.CAP_PROP_AUTO_WB, 0)  # Disable auto white balance
camera.set(cv2.CAP_PROP_WB_TEMPERATURE, 5000)  # Set a custom white balance value (in Kelvin)

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open camera.")
else:
    # Capture a single frame from the camera
    ret, frame = camera.read()

    # Check if the frame was captured successfully
    if ret:
        # Save the captured frame as an image file
        image_filename = "my_image.jpg"
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")
    else:
        print("Error: Could not capture image.")

    # Release the camera
    camera.release()

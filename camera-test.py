import cv2
import datetime

# Set the resolution (width and height)
width, height = 2592, 1944  # Desired resolution

# Set the shutter speed (in microseconds)
shutter_speed = 32955  # 1/30 second exposure time

# Initialize the camera with the specified resolution and format
camera = cv2.VideoCapture(0)
camera.set(3, width)  # Set the width
camera.set(4, height)  # Set the height
camera.set(6, cv2.VideoWriter_fourcc(*'RGB3'))  # Set the image format to TYPE_3BYTE_RGB

# Set the shutter speed (if supported by the camera)
camera.set(cv2.CAP_PROP_EXPOSURE, shutter_speed)

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open camera.")
else:
    # Capture a single frame from the camera
    ret, frame = camera.read()

    # Check if the frame was captured successfully
    if ret:
        # Generate a timestamp for the image filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_filename = f"captured_image_{timestamp}.jpg"

        # Save the frame as an image file with the timestamped filename
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")
    else:
        print("Error: Could not capture image.")

    # Release the camera
    camera.release()

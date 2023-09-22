import time
from capture_image import capture_image
from firebase_uploader import upload_image_to_firebase
from rotate_image import rotate_image

# Define the interval in seconds (10 minutes)
interval_seconds = 10 * 60  # 10 minutes * 60 seconds/minute

# Define the rotation angle
rotation_angle = -2.5  # Rotation angle in degrees

while True:
    # Capture an image and get its path
    image_path = capture_image()
    rotate_image(image_path, rotation_angle)
    upload_image_to_firebase(image_path, image_path)

    time.sleep(interval_seconds)

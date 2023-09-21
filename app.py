import time
from capture_image import capture_image
from firebase_uploader import upload_image_to_firebase

# Define the interval in seconds (10 minutes)
interval_seconds = 10 * 60  # 10 minutes * 60 seconds/minute

while True:
    # Capture an image and get its path
    image_path = capture_image()
    upload_image_to_firebase(image_path, image_path)

    time.sleep(interval_seconds)

import time
from capture_image import capture_image
from rotate_image import rotate_image

# Define the interval in seconds (10 minutes)
interval_seconds = 10 * 60  # 10 minutes * 60 seconds/minute

while True:
    # Capture an image and get its path
    image_path = capture_image()
    rotate_image(image_path)

    time.sleep(interval_seconds)

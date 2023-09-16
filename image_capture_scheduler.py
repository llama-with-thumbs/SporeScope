import time
from capture_image import capture_image

# Define the interval in seconds (30 minutes)
interval_seconds = 30 * 60  # 30 minutes * 60 seconds/minute

while True:
    # Capture an image and get its path
    image_path = capture_image()

    # You can include additional logic here, such as uploading the image to Firebase
    # if image_path is not None:
    #     upload_image_to_firebase(image_path, image_path)

    # Sleep for the specified interval
    time.sleep(interval_seconds)

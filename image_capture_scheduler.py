import schedule
import time
from capture_image import capture_image
# from firebase_uploader import upload_image_to_firebase

schedule.every(0.5).minutes.do(capture_image)

# Keep the script running to allow scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)

    # Capture an image and get its path
    image_path = capture_image()

    # Check if an image has been captured
    # if image_path is not None:
        # Call the upload_image_to_firebase function with the captured image path
        # upload_image_to_firebase(image_path, image_path)

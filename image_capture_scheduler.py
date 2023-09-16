import schedule
import time
from capture_image import capture_image

# Define the interval in minutes (30 minutes)
interval_minutes = 30

# Schedule the capture_image function to run at the specified interval
schedule.every(interval_minutes).minutes.do(capture_image)

# Keep the script running to allow scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)

    # Capture an image and get its path
    image_path = capture_image()

    # You can include additional logic here, such as uploading the image to Firebase
    # if image_path is not None:
    #     upload_image_to_firebase(image_path, image_path)

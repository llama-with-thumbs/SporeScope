import time
from capture_image import capture_image
from firebase_uploader import upload_snippet_to_firebase
from rotate_image import rotate_image
from cut_and_save_snippet import cut_and_save_snippet
# from update_latest_image import update_latest_image
from upload_raw_image import upload_raw_image
from datetime import datetime
from calculate_mean_intensities import calculate_mean_intensities

# Define the interval in seconds (30 minutes)
interval_seconds = 30 * 60  # 30 minutes * 60 seconds/minute

# Define the coordinates for cropping
# x, y, width, height
coordinates_b = [1200, 798, 425, 530]

# Define the rotation angle
rotation_angle = 180  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-8BEA5D1"

# Define flasks names
flask_b = "SMP-A0018B"

while True:
    # Capture an image and get its path
    timestamp = datetime.now().isoformat()

    image_path = capture_image(timestamp)

    rotate_image(image_path, rotation_angle)

    upload_raw_image(image_path, chamber, timestamp)

    # # Call the cut_and_save_rectangle function for each image
    snippet_path_b = cut_and_save_snippet(image_path, coordinates_b, flask_b, chamber)

    upload_snippet_to_firebase(snippet_path_b, flask_b, chamber, timestamp, calculate_mean_intensities(snippet_path_b))

    time.sleep(interval_seconds)

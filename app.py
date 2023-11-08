import time
from capture_image import capture_image
from firebase_uploader import upload_snippet_to_firebase
from rotate_image import rotate_image
from cut_and_save_snippet import cut_and_save_snippet
# from update_latest_image import update_latest_image
from upload_raw_image import upload_raw_image
from datetime import datetime
from calculate_intensity import calculate_intensity

# Define the interval in seconds (30 minutes)
interval_seconds = 30 * 60  # 30 minutes * 60 seconds/minute

# Define the coordinates for cropping
# x, y, width, height
coordinates_a = [410, 868, 425, 530]
coordinates_b = [1060, 868 ,425 ,530]
coordinates_c = [1700, 868 ,425 ,530]

# Define the rotation angle
rotation_angle = 1.2  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-AFBEFC"

# Define flasks names
flask_a = "FLA-2783C2"
flask_b = "FLA-74F078"
flask_c = "FLA-D3610A"

while True:
    # Capture an image and get its path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    image_path = capture_image(timestamp)

    rotate_image(image_path, rotation_angle)

    upload_raw_image(image_path, chamber, timestamp)

    # # Call the cut_and_save_rectangle function for each image
    snippet_path_a = cut_and_save_snippet(image_path, coordinates_a, flask_a, chamber)
    snippet_path_b = cut_and_save_snippet(image_path, coordinates_b, flask_b, chamber)
    snippet_path_c = cut_and_save_snippet(image_path, coordinates_c, flask_c, chamber)

    # update_latest_image(image_path_a)
    # update_latest_image(image_path_b)
    # update_latest_image(image_path_c)

    upload_snippet_to_firebase(snippet_path_a, flask_a, chamber, timestamp, calculate_intensity(snippet_path_a))
    upload_snippet_to_firebase(snippet_path_b, flask_b, chamber, timestamp)
    upload_snippet_to_firebase(snippet_path_c, flask_c, chamber, timestamp)

    time.sleep(interval_seconds)

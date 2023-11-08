import time
from capture_image import capture_image
from firebase_uploader import upload_snippet_to_firebase
from rotate_image import rotate_image
from cut_and_save_snippet import cut_and_save_snippet
from update_latest_image import update_latest_image
from upload_raw_image import upload_raw_image

# Define the interval in seconds (10 minutes)
interval_seconds = 10 * 60  # 10 minutes * 60 seconds/minute

# Define the coordinates for cropping
width = 425
height = 530
y = 868
x1 = 410
x2 = 1060
x3 = 1700

# Define the rotation angle
rotation_angle = 1.2  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-AFBEFC"

flask_a = "FLA-2783C2"
flask_b = "FLA-74F078"
flask_c = "FLA-D3610A"

while True:
    # Capture an image and get its path

    image_path = capture_image()

    rotate_image(image_path, rotation_angle)

    upload_raw_image(image_path, chamber)

    # # Call the cut_and_save_rectangle function for each image
    snippet_path_a = cut_and_save_snippet(image_path, x1, y , width, height, flask_a, chamber)
    # image_path_b = cut_and_save_rectangle(image_path, x2, y , width, height, "B")
    # image_path_c = cut_and_save_rectangle(image_path, x3, y , width, height, "C")

    # update_latest_image(image_path_a)
    # update_latest_image(image_path_b)
    # update_latest_image(image_path_c)

    upload_snippet_to_firebase(snippet_path_a, flask_a, chamber)
    # upload_image_to_firebase(image_path_b, image_path_b)
    # upload_image_to_firebase(image_path_c, image_path_c)

    time.sleep(interval_seconds)

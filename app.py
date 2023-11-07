import time
from capture_image import capture_image
from firebase_uploader import upload_image_to_firebase
from rotate_image import rotate_image
from cut_and_save_rectangle import cut_and_save_rectangle
from update_latest_image import update_latest_image
from upload_raw_image import upload_raw_image

# Define the interval in seconds (10 minutes)
interval_seconds = 10 * 60  # 10 minutes * 60 seconds/minute

# Define the coordinates for cropping
width = 475
height = 550
y=890

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
    # image_path_a = cut_and_save_rectangle(image_path, 1010, y , width, height, "A")
    # image_path_b = cut_and_save_rectangle(image_path, 1660, y , width, height, "B")
    # image_path_c = cut_and_save_rectangle(image_path, 300, y , width, height, "C")

    # update_latest_image(image_path_a)
    # update_latest_image(image_path_b)
    # update_latest_image(image_path_c)

    # upload_image_to_firebase(image_path_a, image_path_a)
    # upload_image_to_firebase(image_path_b, image_path_b)
    # upload_image_to_firebase(image_path_c, image_path_c)

    time.sleep(interval_seconds)

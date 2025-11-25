import time
from datetime import datetime

from core.capture_image import capture_image
from firebase_io.firebase_uploader import upload_snippet_to_firebase
from image_processing.rotate_image import rotate_image
from image_processing.cut_and_save_snippet import cut_and_save_snippet
from firebase_io.upload_raw_image import upload_raw_image
from image_processing.calculate_mean_intensities import calculate_mean_intensities
from image_processing.create_gif_from_images import create_gif_from_images
from firebase_io.upload_gif_file import upload_gif_file
from image_processing.calculate_green_object_area import calculate_green_object_area
from config import (
    INTERVAL_SECONDS,
    COORDINATES,
    ROTATION_ANGLE,
    CHAMBER,
    PLATE_ID,
)

from config import (
    INTERVAL_SECONDS,
    COORDINATES,
    ROTATION_ANGLE,
    CHAMBER,
    PLATE_ID,
)
timestamp = datetime.now().isoformat()
image_path = "test.jpg"

rotate_image(image_path, ROTATION_ANGLE)
upload_raw_image(image_path, CHAMBER, timestamp)

snippet_path = cut_and_save_snippet(image_path, COORDINATES, PLATE_ID, CHAMBER)

upload_snippet_to_firebase(
    snippet_path,
    PLATE_ID,
    CHAMBER,
    timestamp,
    calculate_mean_intensities(snippet_path),
    calculate_green_object_area(snippet_path),
)
create_gif_from_images(f"captured_images/{CHAMBER}/{PLATE_ID}", f"{PLATE_ID}.gif", 200, 0.1, 10)

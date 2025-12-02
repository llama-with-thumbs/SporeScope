import time
from datetime import datetime, timezone

from core.capture_image import capture_image
from firebase_io.firebase_uploader import upload_snippet_to_firebase
from image_processing.rotate_and_crop_image import rotate_and_crop_image
from image_processing.cut_and_save_snippet import cut_and_save_snippet
from firebase_io.upload_raw_image import upload_raw_image
from image_processing.calculate_mean_intensities import calculate_mean_intensities
from image_processing.create_gif_from_images import create_gif_from_images
from firebase_io.upload_gif_file import upload_gif_file
from image_processing.calculate_green_object_area import calculate_green_object_area
from image_processing.cut_and_save_circle_snippets import cut_and_save_circle_snippets
from config import (
    INTERVAL_SECONDS,
    COORDINATES,
    ROTATION_ANGLE,
    CHAMBER,
    PLATE_ID,
    RAW_COORDINATES,
    CIRCLE_COORDS,
    PLATE_START_TIME,
)

def run_capture_loop():
    while True:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        image_path = capture_image(timestamp)

        rotate_and_crop_image(image_path, ROTATION_ANGLE, RAW_COORDINATES)

        upload_raw_image(image_path, CHAMBER, timestamp)

        # snippet_path = cut_and_save_snippet(image_path, COORDINATES, PLATE_ID, CHAMBER)
        
        snippet_paths = cut_and_save_circle_snippets(image_path, CIRCLE_COORDS, PLATE_ID, CHAMBER)
        
        mean_intensities = calculate_mean_intensities(snippet_paths)
        green_object_areas = calculate_green_object_area(snippet_paths)

        upload_snippet_to_firebase(
            snippet_paths,
            PLATE_ID,
            CHAMBER,
            timestamp,
            mean_intensities,
            green_object_areas,
            PLATE_START_TIME
        )
        
        # Create and upload GIFs for each plate in the config list
        for plate in PLATE_ID:
            gif_path = create_gif_from_images(f"captured_images/{CHAMBER}/{plate}", f"{plate}.gif", 200, 0.1, 10)
            # Only attempt upload if GIF creation succeeded
            if gif_path:
                upload_gif_file(gif_path, CHAMBER, plate)
            else:
                print(f"Skipping upload for plate {plate}: GIF not created.")

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    run_capture_loop()

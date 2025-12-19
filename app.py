import time
from datetime import datetime, timedelta, timezone

from ai_integration.chatgpt_client import chatgpt_client
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
from image_processing.calculate_contour import calculate_contour
from image_processing.calculate_contour_areas_mm2 import calculate_contour_areas_mm2
from config import (
    CULTURE,
    INTERVAL_SECONDS,
    COORDINATES,
    ROTATION_ANGLE,
    CHAMBER,
    PLATE_ID,
    RAW_COORDINATES,
    CIRCLE_COORDS,
    PLATE_START_TIME,
    DIAMETER_MM,
    DIAMETER_PX
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

        shapes_lists = []
        total_shapes_area_lists = []

        for snippet_path in snippet_paths:
            shapes = calculate_contour(snippet_path)
            shapes_area = calculate_contour_areas_mm2(shapes)
            shapes_lists.append(shapes)
            total_shapes_area_lists.append(shapes_area)

        elapsed_hours_list = []
        LOCAL_TZ = timezone(timedelta(hours=-5))
        now = datetime.now(LOCAL_TZ)
        for plate_start_time in PLATE_START_TIME:
            start = datetime.fromisoformat(plate_start_time.replace("Z", "+00:00"))
            elapsed_hours = round((now - start).total_seconds() / 3600, 1)
            elapsed_hours_list.append(elapsed_hours)
            
        # get ChatGPT analysis for each plate
        gpt_results = []
        for plate, elapsed_hours, culture, snippet_path in zip(PLATE_ID, elapsed_hours_list, CULTURE, snippet_paths):
            cycle_data = f"""
            Culture: {culture}
            Elapsed time: {elapsed_hours:.2f} hours since inoculation.
            Plate diameter: {DIAMETER_MM} mm 
            """
            gpt_result = chatgpt_client(snippet_path, cycle_data)
            gpt_results.append(gpt_result)

        upload_snippet_to_firebase(
            snippet_paths,
            PLATE_ID,
            CHAMBER,
            timestamp,
            mean_intensities,
            green_object_areas,
            PLATE_START_TIME,
            shapes_lists,
            total_shapes_area_lists,
            gpt_results
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

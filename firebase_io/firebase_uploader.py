import firebase_admin
from firebase_admin import credentials, storage, firestore
import os
import config
import numpy as np


def upload_snippet_to_firebase(
    snippet_paths,
    plates,
    chamber,
    timestamp,
    mean_intensities,
    green_object_areas,
    plate_start_times,
    contours_list,     # NEW
    area_list,         # NEW
):
    """
    Extended to upload contour geometry and computed area.
    """

    # ----------------------------
    # Normalize inputs to lists
    # ----------------------------
    if isinstance(snippet_paths, str):
        snippet_paths = [snippet_paths]

    if not isinstance(mean_intensities, list):
        mean_intensities = [mean_intensities] * len(snippet_paths)

    if not isinstance(green_object_areas, list):
        green_object_areas = [green_object_areas] * len(snippet_paths)

    if not isinstance(contours_list, list):
        contours_list = [contours_list] * len(snippet_paths)

    if not isinstance(area_list, list):
        area_list = [area_list] * len(snippet_paths)

    if len(snippet_paths) != len(plates):
        raise ValueError("snippet_paths and plates must have the same length.")

    if len(mean_intensities) != len(snippet_paths):
        raise ValueError("mean_intensities must match length of snippet_paths.")

    if len(green_object_areas) != len(snippet_paths):
        raise ValueError("green_object_areas must match length of snippet_paths.")

    if len(contours_list) != len(snippet_paths):
        raise ValueError("contours_list must match length of snippet_paths.")

    if len(area_list) != len(snippet_paths):
        raise ValueError("area_list must match length of snippet_paths.")

    # ----------------------------
    # CULTURE handling
    # ----------------------------
    cultures = config.CULTURE
    if isinstance(cultures, str):
        cultures = [cultures]

    if len(cultures) == 1 and len(snippet_paths) > 1:
        cultures *= len(snippet_paths)
    elif len(cultures) != len(snippet_paths):
        raise ValueError("Length of config.CULTURE must be 1 or equal to number of snippet_paths.")

    # ----------------------------
    # PLATE START TIME handling
    # ----------------------------
    if isinstance(plate_start_times, str):
        plate_start_times = [plate_start_times]

    if len(plate_start_times) == 1 and len(snippet_paths) > 1:
        plate_start_times *= len(snippet_paths)
    elif len(plate_start_times) != len(snippet_paths):
        raise ValueError("plate_start_times length mismatch.")

    # ----------------------------
    # Init Firebase
    # ----------------------------
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-adminsdk.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'sporescope.firebasestorage.app'
        })

    bucket = storage.bucket()
    db = firestore.client()

    sporescope_collection = db.collection('sporescope')
    chamber_doc_ref = sporescope_collection.document(chamber)

    chamber_doc_ref.set({
        "chamber": chamber,
        "last_update": timestamp,
    }, merge=True)

    # ----------------------------
    # Loop per snippet / plate
    # ----------------------------
    for (
        snippet_path,
        plate,
        intensity,
        object_area,
        culture,
        plate_start_time,
        contours,
        total_area,
    ) in zip(
        snippet_paths,
        plates,
        mean_intensities,
        green_object_areas,
        cultures,
        plate_start_times,
        contours_list,
        area_list,
    ):
        if intensity is None or object_area is None:
            continue

        mean_red, mean_green, mean_blue = intensity

        local_path = snippet_path.replace("\\", "/")
        filename = os.path.basename(local_path)
        firebase_snippet_path = f"{chamber}/{plate}/{filename}"

        blob = bucket.blob(firebase_snippet_path)
        blob.upload_from_filename(local_path, content_type="image/jpeg")

        gif_path = f"output_gif_folder/{plate}.gif"

        plate_doc_ref = chamber_doc_ref.collection('plates').document(plate)
        plate_doc_ref.set({
            "last_update": timestamp,
            "plate": plate,
            "substrate": config.SUBSTRATE,
            "culture": culture,
            "plate_start_time": plate_start_time,
            "gif_path": gif_path,
            "most_recent_snippet_path": firebase_snippet_path,
        }, merge=True)

        # ----------------------------
        # Serialize contours for Firestore
        # ----------------------------
        serialized_contours = []

        for contour_id, contour in enumerate(contours):
            for p in contour:
                serialized_contours.append({
                    "contour_id": contour_id,
                    "x": int(p[0][0]),
                    "y": int(p[0][1]),
                })

        snippet_fields = {
            "creation_date": timestamp,
            "path": firebase_snippet_path,
            "mean_red_intensity": mean_red,
            "mean_green_intensity": mean_green,
            "mean_blue_intensity": mean_blue,
            "object_area": object_area,
            "total_contour_area": total_area,
            "contours": serialized_contours,
            "plate": plate,
            "chamber": chamber,
            "culture": culture,
            "plate_start_time": plate_start_time,
        }

        plate_doc_ref.collection('snippets').add(snippet_fields)

        print(f"Uploaded snippet + contours for plate {plate}")

    # ----------------------------
    # Cleanup
    # ----------------------------
    if firebase_admin._apps:
        firebase_admin.delete_app(firebase_admin.get_app())

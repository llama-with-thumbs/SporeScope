import firebase_admin
from firebase_admin import credentials, storage, firestore
import os
import config

def upload_snippet_to_firebase(
    snippet_paths,
    plates,
    chamber,
    timestamp,
    mean_intensities,
    green_object_areas,
    plate_start_times,
    shapes_lists,
    total_shapes_area_lists,
    gpt_results
):
    """
    snippet_paths: list of local image paths (one per plate)
    plates: list of plate IDs (e.g. ["PLT-001", "PLT-002"])
    chamber: chamber ID string
    timestamp: ISO timestamp string (capture time)
    mean_intensities: list of (mean_red, mean_green, mean_blue) or single tuple
    green_object_areas: list of numeric areas or single value
    plate_start_times: ISO timestamp string or list of strings
                       (when plate/control was installed), aligned with plates
    shapes_lists: list where each element corresponds to one snippet and contains
                  a list of shapes; each shape is a list of coordinate pairs
    """

    # Normalize inputs to lists
    if isinstance(snippet_paths, str):
        snippet_paths = [snippet_paths]

    if not isinstance(mean_intensities, list):
        mean_intensities = [mean_intensities] * len(snippet_paths)

    if not isinstance(green_object_areas, list):
        green_object_areas = [green_object_areas] * len(snippet_paths)

    if len(snippet_paths) != len(plates):
        raise ValueError("snippet_paths and plates must have the same length.")

    if len(mean_intensities) != len(snippet_paths):
        raise ValueError("mean_intensities must match length of snippet_paths.")

    if len(green_object_areas) != len(snippet_paths):
        raise ValueError("green_object_areas must match length of snippet_paths.")

    # --- CULTURE handling ---
    cultures = config.CULTURE

    if isinstance(cultures, str):
        cultures = [cultures]

    if len(cultures) == 1 and len(snippet_paths) > 1:
        cultures = cultures * len(snippet_paths)
    elif len(cultures) != len(snippet_paths):
        raise ValueError(
            "Length of config.CULTURE must be 1 or equal to number of snippet_paths."
        )

    # --- PLATE START TIME handling ---
    if isinstance(plate_start_times, str):
        plate_start_times = [plate_start_times]

    if len(plate_start_times) == 1 and len(snippet_paths) > 1:
        plate_start_times = plate_start_times * len(snippet_paths)
    elif len(plate_start_times) != len(snippet_paths):
        raise ValueError(
            "Length of plate_start_times must be 1 or equal to number of snippet_paths."
        )

    # --- Init Firebase app once ---
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase-adminsdk.json")
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'sporescope.firebasestorage.app'
            })
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return

    bucket = storage.bucket()
    db = firestore.client()

    # --- Chamber document ---
    sporescope_collection = db.collection('sporescope')
    chamber_doc_ref = sporescope_collection.document(chamber)

    chamber_fields = {
        "chamber": chamber,
        "last_update": timestamp,
    }

    chamber_doc = chamber_doc_ref.get()
    if not chamber_doc.exists:
        chamber_fields["creation_date"] = timestamp

    chamber_doc_ref.set(chamber_fields, merge=True)

    # --- MAIN LOOP ---
    for snippet_path, plate, intensity, object_area, culture, plate_start_time, shapes_list, total_shapes_area, gpt_result in zip(
        snippet_paths, plates, mean_intensities, green_object_areas, cultures, plate_start_times, shapes_lists, total_shapes_area_lists, gpt_results
    ):
        if intensity is None:
            print(f"Skipping plate {plate}: mean_intensities is None for {snippet_path}")
            continue

        if object_area is None:
            print(f"Skipping plate {plate}: green_object_area is None for {snippet_path}")
            continue

        mean_red, mean_green, mean_blue = intensity

        local_path = snippet_path.replace("\\", "/")
        filename = os.path.basename(local_path)

        firebase_snippet_path = f"{chamber}/{plate}/{filename}"

        blob = bucket.blob(firebase_snippet_path)
        blob.upload_from_filename(local_path, content_type="image/jpeg")
        print(f"Image uploaded to Firebase Storage at '{firebase_snippet_path}' for plate {plate}")

        gif_path = f"output_gif_folder/{plate}.gif"

        # Snippet-level fields
        snippet_fields = {
            "creation_date": timestamp,
            "path": firebase_snippet_path,
            "mean_red_intensity": mean_red,
            "mean_green_intensity": mean_green,
            "mean_blue_intensity": mean_blue,
            "object_area": object_area,
            "plate": plate,
            "chamber": chamber,
            "culture": culture,
            "plate_start_time": plate_start_time,
            "total_shape_area_mm2": total_shapes_area
        }

        # Plate document reference
        plate_doc_ref = chamber_doc_ref.collection('plates').document(plate)
        plate_doc_ref.set({
            "last_update": timestamp
        }, merge=True)

        # Snippets subcollection
        snippets_collection_ref = plate_doc_ref.collection('snippets')

        # --- CREATE SNIPPET DOCUMENT FIRST ---
        snippet_doc_ref = snippets_collection_ref.add(snippet_fields)[1]

        # --- SHAPES SUBCOLLECTION ---
        shapes_collection = snippet_doc_ref.collection("shapes")

        for shape_num, contour in enumerate(shapes_list, start=1):
            if hasattr(contour, "squeeze"):
                coords = contour.squeeze().tolist()
            else:
                coords = contour

            cleaned_coords = []
            for p in coords:
                if isinstance(p, (list, tuple)) and len(p) == 1:
                    p = p[0]
                cleaned_coords.append({"x": int(p[0]), "y": int(p[1])})

            shapes_collection.document(f"shape_{shape_num}").set({
                "coordinates": cleaned_coords
            })

        # --- NOW UPDATE PLATE FIELDS BECAUSE snippet_doc_ref EXISTS ---
        plate_fields = {
            "last_update": timestamp,
            "plate": plate,
            "substrate": config.SUBSTRATE,
            "culture": culture,
            "plate_start_time": plate_start_time,
            "gif_path": gif_path,
            "most_recent_snippet_path": firebase_snippet_path,
            "most_recent_snippet_in_firestore_path": snippet_doc_ref.path,
            "total_shape_area_mm2": total_shapes_area,
            "gpt_analysis": gpt_result
        }

        plate_doc_ref.set(plate_fields, merge=True)

        print(f"Document added successfully for plate {plate}.")

    # --- CLEANUP ---
    try:
        if firebase_admin._apps:
            firebase_admin.delete_app(firebase_admin.get_app())
    except Exception as e:
        print(f"Error shutting down Firebase app: {e}")

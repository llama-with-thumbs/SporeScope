import firebase_admin
from firebase_admin import credentials, storage, firestore
import os
import config

def upload_snippet_to_firebase(snippet_paths, plates, chamber, timestamp,
                               mean_intensities, green_object_areas):
    """
    snippet_paths: list of local image paths (one per plate)
    plates: list of plate IDs (e.g. ["PLT-001", "PLT-002"])
    chamber: chamber ID string
    timestamp: ISO timestamp string
    mean_intensities: list of (mean_red, mean_green, mean_blue) or single tuple
    green_object_areas: list of numeric areas or single value
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

    # --- CULTURE handling: associate one culture per snippet/plate ---
    cultures = config.CULTURE  # may be a list or a single string

    # Normalize to list
    if isinstance(cultures, str):
        cultures = [cultures]

    # If only one culture given, reuse it for all snippets
    if len(cultures) == 1 and len(snippet_paths) > 1:
        cultures = cultures * len(snippet_paths)
    elif len(cultures) != len(snippet_paths):
        raise ValueError(
            "Length of config.CULTURE must be 1 or equal to number of snippet_paths."
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

    # --- Chamber doc (shared for all plates) ---
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

    # --- Loop over snippets / plates / cultures ---
    for snippet_path, plate, intensity, object_area, culture in zip(
        snippet_paths, plates, mean_intensities, green_object_areas, cultures
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

        # Storage path for this plate
        firebase_snippet_path = f"{chamber}/{plate}/{filename}"

        # Upload image
        blob = bucket.blob(firebase_snippet_path)
        blob.upload_from_filename(local_path, content_type="image/jpeg")
        print(f"Image uploaded to Firebase Storage at '{firebase_snippet_path}' for plate {plate}")

        # Plate-level fields
        plate_fields = {
            "last_update": timestamp,
            "plate": plate,
            "substrate": config.SUBSTRATE,
            "culture": culture,  # 👈 culture for this plate/snippet
            "most_recent_snippet_path": firebase_snippet_path,
        }

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
            "culture": culture,  # 👈 also store on snippet document
        }

        # Plate doc under chamber
        plate_doc_ref = chamber_doc_ref.collection('plates').document(plate)
        plate_doc_ref.set(plate_fields, merge=True)

        # Snippet subcollection
        snippets_collection_ref = plate_doc_ref.collection('snippets')
        snippets_collection_ref.add(snippet_fields)

        print(f"Document added successfully for plate {plate}.")

    # --- Clean up Firebase app (optional, good for short-lived scripts) ---
    try:
        if firebase_admin._apps:
            firebase_admin.delete_app(firebase_admin.get_app())
    except Exception as e:
        print(f"Error shutting down Firebase app: {e}")

import firebase_admin
from firebase_admin import credentials, storage, firestore
import os
import config

def upload_snippet_to_firebase(image_path, plates, chamber, timestamp, intensity, object_area):
    """
    image_path: local path to snippet image
    plates: list of plate IDs (e.g. ["PLT-001", "PLT-002"])
    chamber: chamber ID string
    timestamp: ISO timestamp string
    intensity: (mean_red, mean_green, mean_blue)
    object_area: numeric area
    """

    # --- Init Firebase app once ---
    try:
        # If no apps initialized yet, init
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase-adminsdk.json")
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'sporescope.firebasestorage.app'
            })
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return

    mean_red, mean_green, mean_blue = intensity

    bucket = storage.bucket()
    db = firestore.client()

    # --- Chamber doc (shared for all plates) ---
    bioChartCollection = db.collection('sporescope')
    chamber_doc_ref = bioChartCollection.document(chamber)

    chamber_fields = {
        "chamber": chamber,
        "last_update": timestamp
    }

    chamber_doc = chamber_doc_ref.get()
    if not chamber_doc.exists:
        chamber_fields["creation_date"] = timestamp

    chamber_doc_ref.set(chamber_fields, merge=True)

    # --- Common local filename ---
    filename = os.path.basename(image_path)
    local_path = image_path.replace("\\", "/")

    # --- Loop over plates ---
    for plate in plates:
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
            "culture": config.CULTURE,
            "most_recent_snippet_path": firebase_snippet_path
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
            "chamber": chamber
        }

        # Plate doc under chamber
        plate_doc_ref = chamber_doc_ref.collection('plates').document(plate)
        plate_doc_ref.set(plate_fields, merge=True)

        # Snippet subcollection
        snippet_doc_ref = plate_doc_ref.collection('snippets')
        snippet_doc_ref.add(snippet_fields)

        print(f"Document added successfully for plate {plate}.")

    # --- Clean up Firebase app (optional, good for short-lived scripts) ---
    try:
        if firebase_admin._apps:
            firebase_admin.delete_app(firebase_admin.get_app())
    except Exception as e:
        print(f"Error shutting down Firebase app: {e}")

import os
import firebase_admin
from firebase_admin import credentials, storage, firestore


def upload_gif_file(gif_path, chamber, plate):
    """Upload a GIF to Firebase Storage and set the plate's gif_path in Firestore.

    This function is defensive:
    - verifies the local file exists
    - initializes the Firebase app only if not already initialized
    - uses set(..., merge=True) to avoid errors if the plate doc does not exist
    - only deletes the app if it initialized it here
    """
    if not os.path.exists(gif_path):
        print(f"Error: GIF file not found: {gif_path}")
        return

    created_app = False
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase-adminsdk.json")
            firebase_admin.initialize_app(cred, {"storageBucket": "sporescope.firebasestorage.app"})
            created_app = True
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        return

    try:
        # Extract the file name from the gif_path
        file_name = os.path.basename(gif_path)

        # Define the category and updated firebase_gif_path
        category = "output_gif_folder"
        firebase_gif_path = f"{category}/{file_name}"

        # Reference to the Firebase Storage bucket
        bucket = storage.bucket()

        # Upload the GIF to Firebase Storage
        blob = bucket.blob(firebase_gif_path.replace("\\", "/"))
        blob.upload_from_filename(gif_path.replace("\\", "/"), content_type="image/gif")

        print(f"GIF uploaded to Firebase Storage at '{firebase_gif_path}'")

        # Create a Firestore client
        db = firestore.client()

        # Add/update the gif_path field on the plate document (merge to avoid overwriting)
        plate_doc_ref = db.collection('sporescope').document(chamber).collection('plates').document(plate)
        plate_doc_ref.set({'gif_path': firebase_gif_path}, merge=True)

        print("Document updated successfully.")

    except Exception as e:
        print(f"Error uploading GIF or updating Firestore: {e}")

    finally:
        # Clean up only if we created the app here
        try:
            if created_app and firebase_admin._apps:
                firebase_admin.delete_app(firebase_admin.get_app())
        except Exception:
            pass

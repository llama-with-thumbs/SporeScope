import os
import firebase_admin
from firebase_admin import credentials, storage, firestore
from datetime import datetime

def upload_gif_file(gif_path):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate("bio-chart-firebase.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

    # Extract the chamber from the gif_path (assuming it's part of the path)
    chamber = os.path.basename(os.path.dirname(os.path.dirname(gif_path)))

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

    # Get the current timestamp
    timestamp = datetime.utcnow().isoformat()

    new_document = {
        "creation date": timestamp,
        "path": firebase_gif_path
    }

    # Add the new document to the specified collection
    db.collection('bio-chart').document(chamber).collection('GIFs').add(new_document)

    print("Document added successfully.")

    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())

# Example usage:
# upload_gif_file("/path/to/gif_file.gif")

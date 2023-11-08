import os
import firebase_admin
from firebase_admin import credentials, storage, firestore

def upload_raw_image(image_path, chamber, timestamp):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate("bio-chart-firebase.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

    # Reference to the Firebase Storage bucket
    bucket = storage.bucket()

    # Extract the file name from the firebase_image_path
    file_name = os.path.basename(image_path)

    # Define the category and updated firebase_image_path
    category = f"{chamber}/Raw images"
    firebase_image_path = f"{category}/{file_name}"

    # Upload the image to Firebase Storage
    blob = bucket.blob(firebase_image_path.replace("\\", "/"))
    blob.upload_from_filename(image_path.replace("\\", "/"), content_type="image/jpeg")

    print(f"Image uploaded to Firebase Storage at '{firebase_image_path}'")

    # Create a Firestore client
    db = firestore.client()

    new_document = {
        "creation date": timestamp,
        "path": firebase_image_path
    }

    # Add the new document to the specified collection
    db.collection('bio-chart').document(chamber).collection('Raw images').add(new_document)

    print("Document added successfully.")

    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())
# Example usage:
# save_raw_image("local_image.jpg", "remote_image.jpg")

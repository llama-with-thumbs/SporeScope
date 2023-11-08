import firebase_admin
from firebase_admin import credentials, storage, firestore
from datetime import datetime


import os

def upload_snippet_to_firebase(image_path, flask, chamber):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate("bio-chart-firebase.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

    # Reference to the Firebase Storage bucket
    bucket = storage.bucket()

    # Get the filename from the input path
    filename = os.path.basename(image_path)

    firebase_snippet_path = f"{chamber}/{flask}/{filename}"
    
    # Upload the image to Firebase Storage
    blob = bucket.blob(firebase_snippet_path)
    blob.upload_from_filename(image_path.replace("\\", "/"), content_type="image/jpeg")

    print("Image uploaded to Firebase Storage at '{}'".format(firebase_snippet_path))


    # Create a Firestore client
    db = firestore.client()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    new_document = {
        "creation date": timestamp,
        "path": firebase_snippet_path
    }

    # Add the new document to the specified collection
    db.collection('bio-chart').document(chamber).collection('flasks').document(flask).collection('snippets').add(new_document)

    print("Document added successfully.")



    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())
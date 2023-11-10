import firebase_admin
from firebase_admin import credentials, storage, firestore
import os

def upload_snippet_to_firebase(image_path, flask, chamber, timestamp, intensity):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate("bio-chart-firebase.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

    mean_red, mean_green, mean_blue = intensity

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

    snippet_fields = {
        "creation_date": timestamp,
        "path": firebase_snippet_path,
        "mean_red_intensity" : mean_red,
        "mean_green_intensity" : mean_green,
        "mean_blue_intensity" : mean_blue,
        "flask": flask,
        "chamber": chamber
    }

    chamber_fields = {
        "creation_date": timestamp,
        "flask": flask,
        "culture": "https://en.wikipedia.org/wiki/Psilocybe_cubensis"
    }

    # Add the new document to the specified collection

    bioChartCollection = db.collection('bio-chart')

    chamberDoc = bioChartCollection.document(chamber).collection('flasks').add(chamber_fields)

    chamberDoc.collection('snippets').add(snippet_fields)

    print("Document added successfully.")



    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())
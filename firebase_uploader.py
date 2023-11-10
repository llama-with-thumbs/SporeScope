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
        "chamber": chamber,
    }

    flask_fields = {
        "last_update": timestamp,
        "flask": flask,
        "substrate": "corn",
        "culture": "https://en.wikipedia.org/wiki/Psilocybe_cubensis"
    }

    # Add the new document to the specified collection

    bioChartCollection = db.collection('bio-chart')

    chamber_doc_ref = bioChartCollection.document(chamber)
    chamber_doc_ref.set(chamber_fields, merge=True)

    # Add the snippet document to the 'snippets' collection within the chamber document
    flask_doc_ref = chamber_doc_ref.collection('flasks').document(flask)
    flask_doc_ref.set(flask_fields)

    snippet_doc_ref = flask_doc_ref.collection('snippets')
    snippet_doc_ref.add(snippet_fields)

    print("Document added successfully.")



    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())
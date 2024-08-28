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

    chamber_fields = {
        "chamber": chamber,
        "last_update": timestamp
    }

    flask_fields = {
        "last_update": timestamp,
        "flask": flask,
        "substrate": "corn",
        "culture": "https://en.wikipedia.org/wiki/Psilocybe_cubensis",
        "most_recent_snippet_path": firebase_snippet_path
    }

    snippet_fields = {
        "creation_date": timestamp,
        "path": firebase_snippet_path,
        "mean_red_intensity" : mean_red,
        "mean_green_intensity" : mean_green,
        "mean_blue_intensity" : mean_blue,
        "flask": flask,
        "chamber": chamber
    }

    
    # Add the new document to the specified collection

    bioChartCollection = db.collection('bio-chart')

    chamber_doc_ref = bioChartCollection.document(chamber)

    chamber_doc_ref.set(chamber_fields, merge=True)

     # Check if the chamber document exists
    chamber_doc = chamber_doc_ref.get()
    if not chamber_doc.exists:
        # If it doesn't exist, set the creation date
        chamber_fields["creation_date"] = timestamp
    
    # Set (or update) the chamber document
    chamber_doc_ref.set(chamber_fields, merge=True)

    # Reference to the flask document within the chamber
    flask_doc_ref = chamber_doc_ref.collection('flasks').document(flask)

    # Check if the flask document exists
    flask_doc = flask_doc_ref.get()
    if not flask_doc.exists:
        # If it doesn't exist, set the creation date
        flask_fields["creation_date"] = timestamp
    
    # Set (or update) the flask document
    flask_doc_ref.set(flask_fields, merge=True)

    # Add the snippet document to the 'snippets' collection within the flask document
    snippet_doc_ref = flask_doc_ref.collection('snippets')
    snippet_fields["creation_date"] = timestamp  # Always set creation_date for snippets
    snippet_doc_ref.add(snippet_fields)
import firebase_admin
from firebase_admin import credentials, storage, firestore
import os

def upload_snippet_to_firebase(image_path, plate, chamber, timestamp, intensity, object_area):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate("firebase-adminsdk.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'sporescope.firebasestorage.app'
    })

    mean_red, mean_green, mean_blue = intensity

    # Reference to the Firebase Storage bucket
    bucket = storage.bucket()

    # Get the filename from the input path
    filename = os.path.basename(image_path)

    firebase_snippet_path = f"{chamber}/{plate}/{filename}"
    
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

    plate_fields = {
        "last_update": timestamp,
        "plate": plate,
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
        "object_area": object_area,
        "plate": plate,
        "chamber": chamber
    }

    
    # Add the new document to the specified collection

    bioChartCollection = db.collection('bio-chart')

    chamber_doc_ref = bioChartCollection.document(chamber)

    # Check if the chamber document exists
    chamber_doc = chamber_doc_ref.get()
    if not chamber_doc.exists:
        # If it doesn't exist, set the creation date
        chamber_fields["creation_date"] = timestamp

    chamber_doc_ref.set(chamber_fields, merge=True)

    # Add the snippet document to the 'snippets' collection within the chamber document
    plate_doc_ref = chamber_doc_ref.collection('plates').document(plate)

    # Check if the plate document exists
    plate_doc = plate_doc_ref.get()
    if not plate_doc.exists:
        plate_fields["gif_path"] = 'gs://bio-chart.appspot.com/CHA-AFBEFC/Gifs/A.gif'
        print("Default gif path added.")

    plate_doc_ref.set(plate_fields, merge=True)
    snippet_doc_ref = plate_doc_ref.collection('snippets')
    snippet_doc_ref.add(snippet_fields)
                
    print("Document added successfully.")

    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())
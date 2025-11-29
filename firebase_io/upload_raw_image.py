import os
import firebase_admin
from firebase_admin import credentials, storage, firestore

def upload_raw_image(image_path, chamber, timestamp):
    # Initialize Firebase Admin SDK only if not already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-adminsdk.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'sporescope.firebasestorage.app'
        })

    bucket = storage.bucket()

    # Ensure proper filename/path
    image_path = image_path.replace("\\", "/")
    file_name = os.path.basename(image_path)

    # If original filename ends with .png, rename it to .png in Firebase
    if file_name.lower().endswith(".png"):
        file_name = file_name[:-4] + ".png"

    # Firebase storage path
    category = f"{chamber}/Raw images"
    firebase_image_path = f"{category}/{file_name}"

    # Upload image as PNG
    blob = bucket.blob(firebase_image_path)
    blob.upload_from_filename(image_path, content_type="image/png")

    print(f"Image uploaded to Firebase Storage at '{firebase_image_path}'")

    # Firestore write
    db = firestore.client()
    db.collection('sporescope').document(chamber).collection('Raw images').add({
        "creation date": timestamp,
        "path": firebase_image_path
    })

    print("Document added successfully.")

    # Shut down Firebase for short-lived scripts
    firebase_admin.delete_app(firebase_admin.get_app())

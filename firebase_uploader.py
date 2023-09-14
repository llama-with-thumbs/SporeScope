import firebase_admin
from firebase_admin import credentials, storage

def upload_image_to_firebase(image_path, firebase_image_path):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate("bio-chart-firebase.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

    # Reference to the Firebase Storage bucket
    bucket = storage.bucket()

    # Upload the image to Firebase Storage
    blob = bucket.blob(firebase_image_path.replace("\\", "/"))
    blob.upload_from_filename(image_path.replace("\\", "/"), content_type="image/jpeg")

    print("Image uploaded to Firebase Storage at '{}'".format(firebase_image_path))

    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())

# Example usage:
# upload_image_to_firebase("local_image.jpg", "images/remote_image.jpg")

import firebase_admin
from firebase_admin import credentials, storage

def download_images_from_firebase_folder(firebase_folder_path, local_directory):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate("bio-chart-firebase.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

    # Reference to the Firebase Storage bucket
    bucket = storage.bucket()

    # List objects (images) in the specified Firebase Storage folder
    blobs = bucket.list_blobs(prefix=firebase_folder_path)

    for blob in blobs:
        # Create the local file path for each image
        local_image_path = local_directory + "/" + blob.name[len(firebase_folder_path):]

        # Download the image from Firebase Storage to the local directory
        blob.download_to_filename(local_image_path.replace("\\", "/"))

        print(f"Downloaded {blob.name} to '{local_image_path}'")

    print("Download complete.")

    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())

# Example usage:
# download_images_from_firebase_folder("captured_images/B/", "local_directory")

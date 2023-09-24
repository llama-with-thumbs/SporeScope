import firebase_admin
from firebase_admin import credentials, storage

def remove_firebase_folder(folder_path):
    try:
        # Initialize Firebase Admin SDK with credentials from "bio-chart-firebase.json"
        cred = credentials.Certificate("bio-chart-firebase.json")
        firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})  # Replace with your bucket URL

        # Reference to the Firebase Storage bucket
        bucket = storage.bucket()

        # List all objects in the specified folder
        blobs = bucket.list_blobs(prefix=folder_path)

        # Delete each object in the folder and print their names
        deleted_file_names = []
        for blob in blobs:
            blob.delete()
            deleted_file_names.append(blob.name)
            print(f"Deleted: {blob.name}")

        print(f"All images in folder '{folder_path}' have been removed from Firebase Storage.")
        print(f"Deleted file names: {', '.join(deleted_file_names)}")

        # End the Firebase session
        firebase_admin.delete_app(firebase_admin.get_app())

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    folder_path = "captured_images/B"  # Replace with the path of the folder you want to clear
    remove_images_from_firebase_folder(folder_path)

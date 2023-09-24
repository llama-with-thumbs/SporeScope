from firebase_uploader import upload_image_to_firebase
from remove_firebase_folder import remove_firebase_folder
import os

def update_latest_image(local_image_path):
    try:

        # Parse local_image_path to extract the folder names and filename
        folder_name = os.path.basename(os.path.dirname(os.path.dirname(local_image_path)))  # Extract another folder name
        subfolder_name = os.path.basename(os.path.dirname(local_image_path))
        subsubfolder_name = "Latest_capture"
        filename = os.path.basename(local_image_path)

        # Remove images from the specified folder in Firebase Storage
        remove_firebase_folder(f"{folder_name}/{subfolder_name}/{subsubfolder_name}")

        # Combine folder names and filename to create firebase_image_path
        firebase_image_path = f"{folder_name}/{subfolder_name}/{subsubfolder_name}/{filename}"

        # Upload the new image to Firebase Storage
        upload_image_to_firebase(local_image_path, firebase_image_path)

    except Exception as e:
        print(f"Error: {str(e)}")

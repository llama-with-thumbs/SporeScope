import re
from firebase_uploader import upload_image_to_firebase
from remove_firebase_folder import remove_firebase_folder

def update_latest_image(local_image_path):
    try:
        # Extract folder names and filename from local_image_path using regular expression
        path_parts = re.split(r'[\\/]', local_image_path)
        folder_name = "captured_images"  # Extract the fourth-to-last element in the path
        subfolder_name = path_parts[-2]  # Extract the third-to-last element in the path
        subsubfolder_name = "Latest_capture"
        filename = path_parts[-1]  # Extract the last element in the path

        # Remove images from the specified folder in Firebase Storage
        remove_firebase_folder(f"{folder_name}/{subfolder_name}/{subsubfolder_name}")

        # Combine folder names and filename to create firebase_image_path
        firebase_image_path = f"{folder_name}/{subfolder_name}/{subsubfolder_name}/{filename}"

        # Upload the new image to Firebase Storage
        upload_image_to_firebase(local_image_path, firebase_image_path)

        print(f"Updated latest image in Firebase Storage. Folder name: {folder_name}, Subfolder name: {subfolder_name}, Filename: {filename}")

    except Exception as e:
        print(f"Error: {str(e)}")

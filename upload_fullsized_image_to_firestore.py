import re
from firebase_uploader import upload_image_to_firebase

def upload_fullsized_image_to_firestore(local_image_path):
    try:
        # Extract folder names and filename from local_image_path using regular expression
        path_parts = re.split(r'[\\/]', local_image_path)
        folder_name = "captured_images"
        subfolder_name = "Full-sized image"
        filename = path_parts[-1]  # Extract the last element in the path

        # Combine folder names and filename to create firebase_image_path
        firebase_image_path = f"{folder_name}/{subfolder_name}/{filename}"

        # Upload the new image to Firebase Storage
        upload_image_to_firebase(local_image_path, firebase_image_path)

        print(f"Updated full-sized image in Firebase Storage. Folder name: {folder_name}, Subfolder name: {subfolder_name}, Filename: {filename}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Example usage:
    local_image_path = "captured_images/captured_image_2023-09-21_16-06-07.jpg"

    upload_fullsized_image_to_firestore(local_image_path)

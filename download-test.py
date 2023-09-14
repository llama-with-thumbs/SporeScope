import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# Initialize Firebase Admin with your credentials
cred = credentials.Certificate("bio-chart-firebase.json")
firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

# Define the file name and path to download

file_name = "captured_images/captured_image_2023-09-01_16-32-00.jpg"
local_file_path = "downloaded_image2.jpg"  # Local file path to save the downloaded image

# Initialize Firebase Storage
bucket = storage.bucket()

# Create a blob object for the file you want to download
blob = bucket.blob(file_name)

# Download the file
try:
    blob.download_to_filename(local_file_path)
    print(f"File downloaded to {local_file_path}")
except Exception as e:
    print(f"Error downloading the file: {str(e)}")

# Clean up: Deinitialize Firebase Admin (optional)
firebase_admin.delete_app(firebase_admin.get_app())

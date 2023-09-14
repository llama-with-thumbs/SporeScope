import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate("bio-chart-firebase.json")
firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

# Reference to the Firebase Storage bucket
bucket = storage.bucket()

# Define local image path
local_image_path = "captured_images/captured_image_2023-09-01_16-32-00.jpg"

# Define the destination path in Firebase Storage
firebase_image_path = "images/captured_image_2023-09-01_16-32-00.jpg"  # Change this to your desired path

# Upload the image to Firebase Storage
blob = bucket.blob(firebase_image_path)
blob.upload_from_filename(local_image_path)

print(f"Image uploaded to Firebase Storage at '{firebase_image_path}'")

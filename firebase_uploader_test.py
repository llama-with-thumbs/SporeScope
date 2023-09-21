import time
from firebase_uploader import upload_image_to_firebase

image_path = "captured_images/750px-Katsura_Imperial_Villa.jpg"
upload_image_to_firebase(image_path, image_path)

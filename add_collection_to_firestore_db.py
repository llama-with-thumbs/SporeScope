import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def add_collection_to_firestore_db(collection_name, timestamp_str, mean_blue_intensity):
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("bio-chart-firebase.json")
    firebase_admin.initialize_app(cred)

    # Create a Firestore client
    db = firestore.client()

    # Convert the timestamp string to a timestamp object
    timestamp = datetime.strptime(timestamp_str, "%Y/%m/%d %H:%M:%S")

    # Convert the timestamp to a string
    timestamp_str = timestamp.strftime("%Y/%m/%d %H:%M:%S")

    # Create a new document with the Timestamp and Mean Blue Intensity fields
    new_document = {
        "Timestamp string": timestamp_str,
        "Mean Blue Intensity": mean_blue_intensity
    }

    # Add the new document to the specified collection
    db.collection(collection_name).add(new_document)

    print("Document added successfully.")

    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())

if __name__ == "__main__":
    # Example usage:
    collection_name = "B_Mean_Blue_Intensity"
    timestamp_str = "2023/09/21 19:07:37"
    mean_blue_intensity = 128.89

    add_collection_to_firestore_db(collection_name, timestamp_str, mean_blue_intensity)

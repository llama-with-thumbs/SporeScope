import firebase_admin
from datetime import datetime
import csv

# Import the add_collection_to_firestore_db function
from add_collection_to_firestore_db import add_collection_to_firestore_db

# Path to the CSV file
csv_file_path = "csv_data\mean_blue_intensity\C_output_data.csv"  # Replace with the actual CSV file name

# Name of the Firestore collection
collection_name = "C_Mean_Blue_Intensity"

# Open and read the CSV file
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Iterate over each row in the CSV
    for row in csv_reader:
        # Extract data from the CSV row
        timestamp_str = row["Timestamp"]
        mean_blue_intensity = float(row["Mean Blue Intensity"])

        # Call the add_collection_to_firestore_db function for each row
        add_collection_to_firestore_db(collection_name, timestamp_str, mean_blue_intensity)

print("Data from CSV file uploaded to Firestore successfully.")

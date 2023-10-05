import cv2
import re
import csv
from pathlib import Path

def calculate_mean_blue_intensity(image_path):
    image = cv2.imread(str(image_path))
    blue_channel = image[:, :, 0]  # Extract the blue channel (0 for blue, 1 for green, 2 for red)
    mean_blue_intensity = blue_channel.mean()
    return mean_blue_intensity

def extract_timestamp(image_filename):
    # Extract the timestamp from the image filename using regular expressions
    # Assuming the timestamp is in the format yyyy-mm-dd_HH-MM-SS (you may need to adjust the pattern)
    match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', image_filename)
    if match:
        timestamp = match.group(1)
        # Split the timestamp into date and time
        date_part, time_part = timestamp.split('_')
        # Format the timestamp as mm/dd/yyyy HH:MM
        formatted_timestamp = f'{date_part.replace("-", "/")} {time_part.replace("-", ":")}'
        return formatted_timestamp
    else:
        return "Unknown"

def main(folder_path, csv_filename):
    folder_path = Path(folder_path)  # Convert the folder path to a pathlib.Path object
    image_files = list(folder_path.glob("*.png")) + list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.jpeg"))

    if not image_files:
        print("No image files found in the folder.")
        return

    mean_blue_intensity_values = []  # Create a list to store mean blue channel intensity values
    timestamps = []  # Create a list to store formatted timestamps

    for image_path in image_files:
        mean_blue_intensity = calculate_mean_blue_intensity(image_path)
        mean_blue_intensity_rounded = round(mean_blue_intensity, 3)  # Round to two decimal places
        mean_blue_intensity_values.append(mean_blue_intensity_rounded)  # Append rounded mean blue intensity value

        # Extract and format the timestamp
        timestamp = extract_timestamp(image_path.stem)
        timestamps.append(timestamp)

        print(f"Image: {image_path.name}, Mean Blue Intensity: {mean_blue_intensity_rounded}, Timestamp: {timestamp}")

    # Create a CSV file and write the data to it
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Timestamp", "Mean Blue Intensity"])  # Write header row
        for i in range(len(image_files)):
            writer.writerow([timestamps[i], mean_blue_intensity_values[i]])

    print(f"Data written to {csv_filename}")

if __name__ == "__main__":
    folder_path = "captured_images/C"  # Replace with the path to your image folder
    csv_filename = "csv_data/mean_blue_intensity/C_output_data.csv"   # Replace with your desired CSV filename
    main(folder_path, csv_filename)

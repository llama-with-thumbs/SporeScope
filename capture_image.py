import os
import picamera
import datetime

# Output directory where the photo will be saved
output_directory = 'captured_images'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Generate a timestamp for the image filename
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
image_filename = "captured_image_" + timestamp + ".jpg"
image_path = os.path.join(output_directory, image_filename)

# Initialize the camera
with picamera.PiCamera() as camera:
    # Capture a photo and save it with the timestamped filename
    camera.capture(image_path)

print("Photo captured and saved as '{}' in '{}' directory.".format(image_filename, output_directory))

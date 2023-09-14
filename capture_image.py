import os
import picamera

# Output directory where the photo will be saved
output_directory = 'captured_images'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize the camera
with picamera.PiCamera() as camera:
    # Capture a photo and save it as "test.jpg" in the output directory
    camera.capture(os.path.join(output_directory, 'test.jpg'))

print("Photo captured and saved as 'test.jpg' in 'captured_images' directory.")

import os
import picamera
import datetime
import time  # Import the time module

def capture_image(output_directory='captured_images'):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Generate a timestamp for the image filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_filename = "captured_image_" + timestamp + ".jpg"
    image_path = os.path.join(output_directory, image_filename)

    try:
        # Initialize the camera
        with picamera.PiCamera() as camera:
            # Set the desired camera settings
            camera.resolution = (2592, 1944)  # Resolution
            camera.brightness = 50  # Brightness
            
            # Set the exposure speed in microseconds (e.g., 32955 for 1/30s)
            camera.shutter_speed = 32955  # Exposure speed in microseconds

            # Wait for the camera settings to stabilize
            camera.exposure_mode = 'auto'  # Set exposure mode to auto
            time.sleep(2)  # Wait for 2 seconds for the settings to take effect
            
            # Capture a photo and save it with the timestamped filename
            camera.capture(image_path)
            print("Image saved as '{}'".format(image_filename))  # Print the filename

        return image_path  # Return the path of the saved image
    except Exception as e:
        print("Error: {}".format(e))
        return None  # Return None if the image capture fails

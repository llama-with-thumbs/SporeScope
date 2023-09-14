import os
import datetime
import picamera

def capture_image(output_directory='captured_images'):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Generate a timestamp for the image filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_filename = "captured_image_" + timestamp + ".jpg"
    image_path = os.path.join(output_directory, image_filename)

    # Initialize the camera
    with picamera.PiCamera() as camera:
        # Capture an image and save it to the specified path
        camera.capture(image_path)
        print("Image saved at {}".format(image_path))  # Using string formatting

    # Return the path of the saved image
    return image_path

# Example usage:
# image_path = capture_image()

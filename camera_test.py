import picamera

def capture_image(image_filename):
    try:
        # Initialize the camera
        with picamera.PiCamera() as camera:
            # Set the resolution (adjust as needed)
            camera.resolution = (1920, 1080)  # Example resolution

            # Capture the image and save it
            camera.capture(image_filename)
            print(f"Image saved as {image_filename}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the image filename
    image_filename = "my_image.jpg"

    # Call the capture_image function with the desired filename
    capture_image(image_filename)

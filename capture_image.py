import subprocess
import os

def capture_image(timestamp, output_directory='captured_images'):
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Capture an image using fswebcam
        image_filename = f"captured_image_{timestamp}.jpg"
        image_path = os.path.join(output_directory, image_filename)

        subprocess.run(["fswebcam", "-r", "2592x1944", "--no-banner", image_path])

        # Return the path of the captured image
        return image_path
    except Exception as e:
        print(f"Error capturing image: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    image_path = capture_image()
    if image_path:
        print(f"Image saved as {image_path}")
    else:
        print("Image capture failed.")

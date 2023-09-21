import subprocess
import datetime

# Capture an image using fswebcam
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
image_filename = f"captured_image_{timestamp}.jpg"
subprocess.run(["fswebcam", "-r", "2592x1944", "--no-banner", image_filename])

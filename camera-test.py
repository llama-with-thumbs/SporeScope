import picamera
import time

# Initialize the camera
camera = picamera.PiCamera()

# Capture an image (this will use automatic exposure settings)
camera.capture('auto_exposure.jpg')

# Retrieve the actual exposure time in microseconds
exposure_speed = camera.exposure_speed

# Close the camera
camera.close()

# Print the exposure time
print("Automatic Exposure Time: {} microseconds".format(exposure_speed))

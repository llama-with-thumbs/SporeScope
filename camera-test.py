import picamera
import time

# Initialize the camera
camera = picamera.PiCamera()

# Capture an image (this will use automatic exposure settings)
camera.capture('auto_exposure.jpg')

# Retrieve the actual exposure time in microseconds
exposure_speed = camera.exposure_speed

# Get the image metadata
image_metadata = {
    "Resolution": camera.resolution,
    "Exposure Mode": camera.exposure_mode,
    "Exposure Compensation": camera.exposure_compensation,
    "ISO": camera.iso,
    "Shutter Speed (microseconds)": camera.shutter_speed,
    "Meter Mode": camera.meter_mode,
    "AWB (Auto White Balance) Mode": camera.awb_mode,
    "Image Effect": camera.image_effect,
    "Contrast": camera.contrast,
    "Brightness": camera.brightness,
    "Saturation": camera.saturation,
    "Sharpness": camera.sharpness,
    "Annotate Text": camera.annotate_text,
    "Framerate": camera.framerate,
    "Rotation": camera.rotation,
    "Sensor Mode": camera.sensor_mode,
}

# Close the camera
camera.close()

# Save the image metadata to a text file
with open('image_metadata.txt', 'w') as metadata_file:
    for key, value in image_metadata.iteritems():
        metadata_file.write("{}: {}\n".format(key, value))

# Print the exposure settings for the captured image
print("Exposure Settings for Captured Image:")
print("Exposure Speed for Captured Image: {} microseconds".format(exposure_speed))

import picamera

# Initialize the camera
camera = picamera.PiCamera()

# Print Camera Settings
print("Camera Settings:")
print("Resolution: {}".format(camera.resolution))
print("Exposure Mode: {}".format(camera.exposure_mode))
print("Exposure Compensation: {}".format(camera.exposure_compensation))
print("ISO: {}".format(camera.iso))
print("Shutter Speed: {} microseconds".format(camera.shutter_speed))
print("Meter Mode: {}".format(camera.meter_mode))
print("AWB (Auto White Balance) Mode: {}".format(camera.awb_mode))
print("Image Effect: {}".format(camera.image_effect))
print("Contrast: {}".format(camera.contrast))
print("Brightness: {}".format(camera.brightness))
print("Saturation: {}".format(camera.saturation))
print("Sharpness: {}".format(camera.sharpness))
print("Annotate Text: {}".format(camera.annotate_text))
print("Framerate: {}".format(camera.framerate))
print("Rotation: {}".format(camera.rotation))
print("Sensor Mode: {}".format(camera.sensor_mode))

# Close the camera
camera.close()

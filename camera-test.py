import picamera

# Initialize the camera
camera = picamera.PiCamera()

# Print Camera Settings
print("Camera Settings:")
print(f"Resolution: {camera.resolution}")
print(f"Exposure Mode: {camera.exposure_mode}")
print(f"Exposure Compensation: {camera.exposure_compensation}")
print(f"ISO: {camera.iso}")
print(f"Shutter Speed: {camera.shutter_speed} microseconds")
print(f"Meter Mode: {camera.meter_mode}")
print(f"AWB (Auto White Balance) Mode: {camera.awb_mode}")
print(f"Image Effect: {camera.image_effect}")
print(f"Contrast: {camera.contrast}")
print(f"Brightness: {camera.brightness}")
print(f"Saturation: {camera.saturation}")
print(f"Sharpness: {camera.sharpness}")
print(f"Annotate Text: {camera.annotate_text}")
print(f"Framerate: {camera.framerate}")
print(f"Rotation: {camera.rotation}")
print(f"Sensor Mode: {camera.sensor_mode}")

# Close the camera
camera.close()

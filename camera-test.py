import picamera

# Initialize the camera
camera = picamera.PiCamera()

# Get a list of all camera characteristics
characteristics = dir(camera)

# Print the list of characteristics and their values
print("List of Camera Characteristics and Their Values:")
for char in characteristics:
    if not callable(getattr(camera, char)):  # Check if it's not a method
        value = getattr(camera, char)
        print("{}: {}".format(char, value))

# Close the camera
camera.close()

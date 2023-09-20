import picamera

# Initialize the camera
camera = picamera.PiCamera()

# Get a list of all camera characteristics
characteristics = dir(camera)

# Print the list of characteristics
print("List of Camera Characteristics:")
for char in characteristics:
    print(char)

# Close the camera
camera.close()

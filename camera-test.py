import cv2

# Initialize the camera
camera = cv2.VideoCapture(0)

# Capture a single frame
ret, frame = camera.read()

# Save the captured frame as an image
if ret:
    cv2.imwrite('my_image.jpg', frame)
else:
    print('Error capturing image')

# Release the camera
camera.release()

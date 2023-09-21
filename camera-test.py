import cv2

# Initialize the camera
camera = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open camera.")
else:
    # Capture a single frame from the camera
    ret, frame = camera.read()

    # Check if the frame was captured successfully
    if ret:
        # Save the captured frame as an image file
        image_filename = "my_image.jpg"
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")
    else:
        print("Error: Could not capture image.")

# Release the camera
camera.release()

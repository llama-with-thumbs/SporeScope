import cv2
import numpy as np

# Load the image (assuming 'test.jpg' is the original image)
image = cv2.imread('test.jpg')

# Resize the image to 425px x 530px if needed
image = cv2.resize(image, (425, 530))

# Convert the image to HSV color space to better detect the green color
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range of green color in HSV (you may adjust the values)
lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

# Create a mask for green objects
mask = cv2.inRange(hsv, lower_green, upper_green)

# Apply minimal Gaussian Blur (using a small kernel size for minimal smoothing)
mask = cv2.GaussianBlur(mask, (3, 3), 0)

# Bitwise-AND mask and original image to isolate the green object
green_object = cv2.bitwise_and(image, image, mask=mask)

# Convert the mask to grayscale for contour detection
gray_mask = cv2.cvtColor(green_object, cv2.COLOR_BGR2GRAY)

# Find contours in the masked grayscale image
contours, _ = cv2.findContours(gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the original image to draw the contours
contour_image = image.copy()

# Variable to store the total surface area of the object(s)
total_area = 0

# Loop through each contour, calculate area, and approximate for smoother edges
for contour in contours:
    # Calculate the area of the contour
    area = cv2.contourArea(contour)
    total_area += area  # Add the area to the total

    # Use contour approximation to make the contours smoother
    epsilon = 0.002 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Draw the approximated contour on the image
    cv2.drawContours(contour_image, [approx], -1, (0, 255, 0), 2)

# Convert the total area to string and print it on the image
area_text = f"Area: {int(total_area)} pixels"
cv2.putText(contour_image, area_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Display the results
cv2.imshow('Contours with Area', contour_image)

# Wait for a key press and close the image windows
cv2.waitKey(0)
cv2.destroyAllWindows()

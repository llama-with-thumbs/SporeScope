import cv2
import numpy as np

def find_contours(image, lower_color, upper_color):
    # Convert the image to HSV color space to better detect the target color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply minimal Gaussian Blur (using a small kernel size for minimal smoothing)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)

    # Find contours in the masked grayscale image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def draw_translucent_contours(base_image, contours, color, alpha=0.5):
    # Create a blank overlay with the same size as the base image
    overlay = base_image.copy()

    # Draw filled contours on the overlay
    for contour in contours:
        cv2.drawContours(overlay, [contour], -1, color, thickness=cv2.FILLED)

    # Blend the overlay with the base image using the alpha (transparency) factor
    cv2.addWeighted(overlay, alpha, base_image, 1 - alpha, 0, base_image)

# Load two images (assuming 'test.jpg' and 'test1.jpg' are the original images)
image1 = cv2.imread('test.jpg')
image2 = cv2.imread('test1.jpg')

# Resize both images to the same dimensions (425px x 530px in this case)
image1 = cv2.resize(image1, (425, 530))
image2 = cv2.resize(image2, (425, 530))

# Define the range of green color in HSV for contour detection
lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

# Find contours in both images
contours1 = find_contours(image1, lower_green, upper_green)
contours2 = find_contours(image2, lower_green, upper_green)

# Create a blank image (black background) to draw the contours
overlap_image = np.zeros_like(image1)

# Draw translucent blue contours for image1
draw_translucent_contours(overlap_image, contours1, (255, 0, 0), alpha=0.5)  # Blue with 50% opacity

# Draw translucent yellow contours for image2
draw_translucent_contours(overlap_image, contours2, (0, 255, 255), alpha=0.5)  # Yellow with 50% opacity

# Draw green outlines for contours in both images
for contour in contours1 + contours2:
    cv2.drawContours(overlap_image, [contour], -1, (0, 255, 0), 2)  # Green outline for both contours

# Display the result (blue and yellow translucent contours with green outlines)
cv2.imshow('Overlapped Translucent Contours', overlap_image)

# Wait for a key press and close the image windows
cv2.waitKey(0)
cv2.destroyAllWindows()

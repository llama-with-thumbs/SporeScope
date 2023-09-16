import cv2
import numpy as np

# Load the image
image = cv2.imread('./captured_images/captured_image_2023-09-15_14-27-40.jpg')

# Define the coordinates and dimensions for cropping the object
start_x = 230    # X-coordinate of the top-left corner
start_y = 140    # Y-coordinate of the top-left corner
width = 210      # Width of the object region (210 pixels)
height = 280     # Height of the object region (280 pixels)

# Crop the specified region
object_region = image[start_y:start_y + height, start_x:start_x + width]

# Convert the image to grayscale
gray = cv2.cvtColor(object_region, cv2.COLOR_BGR2GRAY)

# Apply a threshold to create a binary mask
_, thresholded = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

# Ensure the mask has the correct data type
object_mask = np.uint8(thresholded)

# Invert the mask to create the background
background_mask = cv2.bitwise_not(object_mask)

# Create a white background
background = np.full_like(object_region, (255, 255, 255), dtype=np.uint8)

# Replace the background with white
result = cv2.bitwise_and(object_region, object_region, mask=object_mask)
result += cv2.bitwise_and(background, background, mask=background_mask)

# Display the result (optional)
cv2.imshow('Object with Removed Background', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the result
output_path = './captured_images/object_with_removed_background.jpg'
cv2.imwrite(output_path, result)

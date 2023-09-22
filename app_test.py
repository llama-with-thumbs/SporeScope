from rotate_image import rotate_image
from cut_and_save_rectangle import cut_and_save_rectangle

# Define the image file path and rotation angle
image_file_path = "captured_image_2023-09-21_16-56-33.jpg"
rotation_angle = -2.5  # Rotation angle in degrees

# Call the rotate_image function
try:
    rotated_image = rotate_image(image_file_path, rotation_angle)
    cut_and_save_rectangle(image_file_path)
    print("Rotated and saved:", image_file_path)
    if rotated_image is not None:
        print("Image rotation failed.")
    else:
        print("Image rotated successfully.")
except Exception as e:
    print(f"Error: {e}")

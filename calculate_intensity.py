import cv2

def calculate_intensity(image_path):
    image = cv2.imread(str(image_path))
    blue_channel = image[:, :, 0]  # Extract the blue channel (0 for blue, 1 for green, 2 for red)
    mean_blue_intensity = blue_channel.mean()
    return mean_blue_intensity
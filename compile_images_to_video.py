import cv2
import os
import datetime

def compile_images_into_video(image_directory, output_video_path, frame_rate):
    image_files = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]
    image_files.sort()  # Ensure filenames are sorted in numerical order

    if len(image_files) == 0:
        print("No image files found in the directory.")
        return

    first_image = cv2.imread(os.path.join(image_directory, image_files[0]))
    height, width, _ = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        frame = cv2.imread(image_path)
        video_writer.write(frame)

    video_writer.release()
    print(f"Video saved at {output_video_path}")

def create_and_compile_video_folder(input_image_directory, output_folder='compiled_videos', frame_rate=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_video_path = os.path.join(output_folder, f"video_{timestamp}.avi")

    compile_images_into_video(input_image_directory, output_video_path, frame_rate)

if __name__ == "__main__":
    input_image_directory = 'captured_images/A'
    create_and_compile_video_folder(input_image_directory)

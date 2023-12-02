from compile_images_to_video import compile_images_into_video
from firebase_storage_image_downloader import download_images_from_firebase_folder
from create_gif_from_images import create_gif_from_images
sample = "A"

# download_images_from_firebase_folder(f"captured_images/{sample}", f"captured_images/{sample}")
# compile_images_into_video(f"captured_images/{sample}", f"captured_images/{sample}.avi", 20)
create_gif_from_images(f"captured_images/{sample}", f"{sample}.gif", 200, 0.01, 1)
from PIL import Image, ImageDraw

def draw_circles_on_image(image_path, circles, output_path="test_with_circles.png"):
    """
    image_path: path to the input image
    circles: list of (x, y, r) triplets
    output_path: filename for the saved output image
    """
    img = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    for (cx, cy, r) in circles:
        bbox = (cx - r, cy - r, cx + r, cy + r)
        draw.ellipse(bbox, outline="red", width=4)

    img.save(output_path)
    print(f"Saved image with circles: {output_path}")


if __name__ == "__main__":
    image_path = "test.png"

    circles = [
        (505, 455, 250),
        (1065, 450, 250),
    ]

    draw_circles_on_image(image_path, circles)

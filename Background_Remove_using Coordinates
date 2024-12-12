import requests
from PIL import Image, ImageOps
from io import BytesIO
from rembg import remove


def process_image_from_url_with_bbox(image_url, bounding_box, output_path="output.png"):
    
    try:
        # Step 1: Download the image from the URL
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            input_image = Image.open(BytesIO(response.content)).convert("RGBA")

            # Step 2: Crop the image using bounding box
            x_min = bounding_box["x_min"]
            y_min = bounding_box["y_min"]
            x_max = bounding_box["x_max"]
            y_max = bounding_box["y_max"]
            cropped_region = input_image.crop((x_min, y_min, x_max, y_max))

            # Step 3: Remove the background from the cropped region
            cropped_bytes = BytesIO()
            cropped_region.save(cropped_bytes, format="PNG")
            cropped_output = remove(cropped_bytes.getvalue())

            # Step 4: Convert back to image and paste onto the original image
            processed_region = Image.open(BytesIO(cropped_output)).convert("RGBA")
            transparent_image = Image.new("RGBA", input_image.size, (0, 0, 0, 0))
            transparent_image.paste(processed_region, (x_min, y_min))

            # Step 5: Save the final image as PNG
            transparent_image.save(output_path)
            print(f"Processed image saved to {output_path}")
        else:
            print(f"Failed to fetch image. HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example Usage
image_url = "https://plus.unsplash.com/premium_photo-1681449856688-2abd99ab5a73?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
bounding_box = {
    "x_min": 100,
    "y_min": 50,
    "x_max": 800,
    "y_max": 600,
}
process_image_from_url_with_bbox(image_url, bounding_box, "output.png")

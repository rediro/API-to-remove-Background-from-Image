import requests
from rembg import remove


def process_image_from_url(image_url, output_path="output.png"):

    try:
        # Step 1: Download the image from the URL
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True

            # Step 2: Read the image data
            input_image = response.content

            # Step 3: Remove the background
            output_image = remove(input_image)

            # Step 4: Save the processed image as PNG
            with open(output_path, 'wb') as output_file:
                output_file.write(output_image)

            print(f"Processed image saved to {output_path}")
        else:
            print(f"Failed to fetch image. HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example Usage
image_url = "https://plus.unsplash.com/premium_photo-1681449856688-2abd99ab5a73?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
process_image_from_url(image_url, "output.png")

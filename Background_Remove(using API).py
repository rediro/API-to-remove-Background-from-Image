import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
from rembg import remove
from google.cloud import storage
import datetime

# Initialize the FastAPI app
app = FastAPI()

# Configure Google Cloud Storage
BUCKET_NAME = "image-bg-removal-bucket"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/tanmay/practice/API to remove Background from Image/app/image-bg-removal-7ed1cbc09666.json"

# Input model for API
class ImageProcessRequest(BaseModel):
    image_url: str
    bounding_box: dict

# Utility to upload to GCS and generate signed URL
def upload_to_gcs(bucket_name, source_file, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(source_file)

    # Generate a signed URL that will expire in 1 hour
    expiration_time = datetime.timedelta(hours=1)
    signed_url = blob.generate_signed_url(
        expiration=expiration_time,
        method='GET',
        version='v4'
    )

    return signed_url

# Route for processing image
@app.post("/process-image")
async def process_image(req: ImageProcessRequest):
    try:
        # Download the image from the URL
        response = requests.get(req.image_url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch image")

        # Open image and apply cropping
        input_image = Image.open(BytesIO(response.content)).convert("RGBA")
        bbox = req.bounding_box
        x_min, y_min, x_max, y_max = bbox["x_min"], bbox["y_min"], bbox["x_max"], bbox["y_max"]

        # Validate bounding box coordinates
        if x_min >= x_max or y_min >= y_max or x_max > input_image.width or y_max > input_image.height:
            raise HTTPException(status_code=400, detail="Invalid bounding box coordinates")

        cropped_region = input_image.crop((x_min, y_min, x_max, y_max))

        # Remove background
        cropped_bytes = BytesIO()
        cropped_region.save(cropped_bytes, format="PNG")
        cropped_output = remove(cropped_bytes.getvalue())

        # Reconstruct transparent image
        processed_region = Image.open(BytesIO(cropped_output)).convert("RGBA")
        transparent_image = Image.new("RGBA", input_image.size, (0, 0, 0, 0))
        transparent_image.paste(processed_region, (x_min, y_min))

        # Save output locally
        output_path = "output.png"
        transparent_image.save(output_path)

        # Upload to GCS and get the signed URL
        public_url = upload_to_gcs(BUCKET_NAME, output_path, f"processed_images/{os.path.basename(output_path)}")

        return {
            "original_image_url": req.image_url,
            "processed_image_url": public_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

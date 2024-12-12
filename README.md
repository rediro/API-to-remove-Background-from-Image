# API-to-remove-Background-from-Image
An API to remove image backgrounds for e-commerce platforms. Accepts a public image URL and bounding box coordinates, processes the image to remove the background, and returns a transparent PNG hosted on Google Cloud Storage. Built using FastAPI, rembg, and PIL, with scalable deployment via Docker and Google Cloud Run.


API Hosting:
You have successfully deployed the API to Google Cloud, and your endpoint is live at:

Live API endpoint: https://image-bg-removal.de.r.appspot.com

#How to Test the API:
To test the API, you can use tools like Postman . Below is a step-by-step guide to help you with that:

Example Request using Postman:
Set HTTP Method to POST

URL: https://image-bg-removal.de.r.appspot.com/process-image
Headers:
Content-Type: application/json
Body:
json

{
    "image_url": "https://plus.unsplash.com/premium_photo-1681449856688-2abd99ab5a73?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "bounding_box": {
        "x_min": 500,
        "y_min": 500,
        "x_max": 1000,
        "y_max": 1000
    }
}
Expected Response:
If the request is successful, you will get the following response with the original image URL and the URL of the processed image:

json

{
    "original_image_url": "https://plus.unsplash.com/premium_photo-1681449856688-2abd99ab5a73?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "processed_image_url": "<signed_url_of_processed_image>"
}
<img width="1440" alt="Screenshot 2024-12-12 at 1 14 40 AM" src="https://github.com/user-attachments/assets/44d20cba-dcd0-4b92-b9c1-f30f82e13af1" />

<img width="1440" alt="Screenshot 2024-12-12 at 1 15 52 AM" src="https://github.com/user-attachments/assets/a705d8d1-f389-49d7-bcff-9d342dbcf98b" />

If there’s an error (e.g., invalid URL or bounding box), you will get an error message:

json

{
    "error": "<error_message>"
}<img width="1440" alt="Screenshot 2024-12-12 at 10 55 49 AM" src="https://github.com/user-attachments/assets/bdce21ab-0d92-4dad-ba8d-0f1f1eab3b62" />

Postman Collection:
You can create a Postman collection for your API with the following details:

Request URL: https://image-bg-removal.de.r.appspot.com/process-image
Method: POST
Body Type: raw
Body Content (JSON):
json

{
    "image_url": "<public_image_url>",
    "bounding_box": {
        "x_min": <integer>,
        "y_min": <integer>,
        "x_max": <integer>,
        "y_max": <integer>
    }
}

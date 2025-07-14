# dalle.py

import openai
import requests
import os
from PIL import Image
from io import BytesIO

def save_image(image_url):
    
    response = requests.get(image_url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save("output/saved_image.jpg")
    else:
        print("Failed to download image.")


def generate_image(client, prompt, model, size,
                   quality,
                   style):
    """
    Generates an image based on a prompt using OpenAI's DALL-E model.

    Returns:
    str: The path to the generated image.
    """
    result = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        style=style
    )

    json_response = json.loads(result.model_dump_json())
    image_url = json_response["data"][0]["url"]

    return image_url

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     image_path = generate_image()

#     print(f"Generated image saved at: {image_path}")

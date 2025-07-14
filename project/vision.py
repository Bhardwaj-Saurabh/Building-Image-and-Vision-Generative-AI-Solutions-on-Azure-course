# vision.py

import openai

# Function to describe the generated image and annotate issues

def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(
            image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{base64_encoded_data}"


def describe_image(client, image_path, deployment_name, prompt):
    """
    Describes an image and identifies key visual elements related to the customer complaint.

    Returns:
    str: A description of the image, including the annotated details.
    """
    data_url = local_image_to_data_url(image_path)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     description = describe_image()
#     print(description)

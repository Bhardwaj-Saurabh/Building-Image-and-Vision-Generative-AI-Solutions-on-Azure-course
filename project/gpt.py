# gpt.py

import openai

# Function to classify the customer complaint based on the image description

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")


def classify_with_gpt(client, deployment_name, prompt):
    """
    Classifies the customer complaint into a category/subcategory based on the image description.

    Returns:
    str: The category and subcategory of the complaint.
    """
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1000
    )

    result = response.choices[0].message.content
    return result

    

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     classification = classify_with_gpt()
#     print(classification)

# main.py

# Import functions from other modules
from whisper import transcribe_audio
from dalle import generate_image
from vision import describe_image
from gpt import classify_with_gpt
from dotenv import load_env
import json

load_env()
# Main function to orchestrate the workflow

# Function to generate an image representing the customer complaint
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
delle_model = "dall-e-3"
delle_api_version="2024-02-01"

gpt_deployment_id = "gpt-4.1-mini"
gpt_api_version="2024-12-01-preview"

whisper_deployment_id = "whisper"
whisper_api_version="2024-06-01"

def create_openai_client(api_version, api_key, api_endpoint):
    client = AzureOpenAI(
        api_version=api_version,
        api_key=api_key,
        azure_endpoint=api_endpoint
    )
    return client

whisper_client = create_openai_client(whisper_api_version, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
delle_client = create_openai_client(delle_api_version, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
vision_client = create_openai_client(gpt_api_version, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
chat_client = create_openai_client(gpt_api_version, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)



def main():
    """
    Orchestrates the workflow for handling customer complaints.
    
    Steps include:
    1. Transcribe the audio complaint.
    2. Create a prompt from the transcription.
    3. Generate an image representing the issue.
    4. Describe the generated image.
    5. Annotate the reported issue in the image.
    6. Classify the complaint into a category/subcategory pair.
    
    Returns:
    None
    """
    # TODO: Call the function to transcribe the audio complaint.
    audio_file_path = "project/audio"
    transcribed_audio_text = transcribe_audio(whisper_client, audio_file_path, whisper_deployment_id)

    print('t - done')

    # TODO: Create a prompt from the transcription prompt
    image_prompt = f"""You are an expert image generator. You are tasked with creating an image based on the complains. 
                        The main context of the customer complain is given below.
                        {transcribed_audio_text}
                        
                        Understand the transcribed_audio_text well and create an image reflecting the text."""

    # TODO: Generate an image based on the prompt.
    image_url = generate_image(delle_client, 
                            prompt, 
                            delle_model, 
                            size = '1024x1024',
                            quality = 'hd',
                            style = 'natural')

    print('image - done')

    # TODO: Describe the generated image.
    description_prompt = "Analyse and describe the image to provide detailed descriptions of their contents."
    image_description = describe_image(vision_client, image_url, gpt_deployment_id, prompt)

    print('des - done')

    # TODO: Annotate the reported issue in the image.

    # TODO: Classify the complaint based on the image description.
    with open("data.json", "r", encoding="utf-8") as file:
        categories = json.load(file)

    response_prompt = f""" You are an helpful assistant who help to indentify and classify the customer complains based on the provided image description. 

    ## Task
    Use the below provides image description to indentify the category and sub category. 

    - You must only use provided Categories and Subcategories to classify the image. 
    - If you do not have the answer, just say 'No category available'

    ## Image Description 
    {image_description}

    ##Categories and Subcategories
    {categories}

    ## Output Format

    ```json
    category : the main ctegory from the provided categories
        - subcategory: subcategory from the provided subcategories
    ```
    """
    # final_response = classify_with_gpt(chat_client, gpt_deployment_id, prompt)

    # TODO: Print or store the results as required.

    # Replace this with your implementation

# Example Usage (for testing purposes, remove/comment when deploying):
if __name__ == "__main__":
    main()

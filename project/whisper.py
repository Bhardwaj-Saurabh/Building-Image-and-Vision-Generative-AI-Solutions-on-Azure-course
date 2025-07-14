# whisper.py
import os
import openai

# Function to transcribe customer audio complaints using the Whisper model


def transcribe_audio(client, audio_file_path, deployment_id):
    """
    Transcribes an audio file into text using Azure OpenAI's Whisper model.

    Parameters:
    client: azure api client
    audio_file_path (str): Path to the audio file to be transcribed.
    deployment_id (str): Deployment ID of the Whisper model.

    Returns:
    str: The transcribed text of the audio file.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.Audio.transcribe(
                deployment_id=deployment_id,
                file=audio_file
            )
        return response["text"]
    except Exception as e:
        return f"An error occurred during transcription: {e}"


# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     transcription = transcribe_audio()
#     print(transcription)

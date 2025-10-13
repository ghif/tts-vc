import os
from dotenv import load_dotenv
load_dotenv()

from google.cloud import texttospeech_v1beta1 as texttospeech
from google.api_core.client_options import ClientOptions

import tempfile

from vc import VoiceCloner
import torch
import torchaudio as ta

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

DEVICE = "cpu"
if torch.cuda.is_available():
    DEVICE = "cuda"

if torch.backends.mps.is_available():
    DEVICE = "mps"
    
# Load voice cloning model
cloning_model = VoiceCloner.from_pretrained(DEVICE)


PROJECT_ID = os.getenv("PROJECT_ID")
TTS_LOCATION = os.getenv("TTS_LOCATION")
API_ENDPOINT = (
    f"{TTS_LOCATION}-texttospeech.googleapis.com"
    if TTS_LOCATION != "global"
    else "texttospeech.googleapis.com"
)

def generate_speech(text, voice="Leda", language_code="id-ID"):
    """
    Generate speech using Google's Chirp 3 Text-to-Speech API

    Args:
        text (str): The text to be synthesized.
        voice (str): The name of the voice to use (e.g., "Leda", "Charon").
        language_code (str): The language code for the voice (e.g., "id-ID" for Indonesian, "en-US" for English).
    Returns:
        bytes: The synthesized speech audio in MP3 format.
        
    """
    # Obtain default credentials and create an authorized session
    voice_name = f"{language_code}-Chirp3-HD-{voice}"
    voice = texttospeech.VoiceSelectionParams(
        name=voice_name,
        language_code=language_code,
    )

    # Initialize the TTS client with the specified API endpoint
    client = texttospeech.TextToSpeechClient(
        client_options=ClientOptions(api_endpoint=API_ENDPOINT)
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=text),
        voice=voice,
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        ),
    )

    # Create a temporary MP3 file
    audio_content = response.audio_content

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_content)
        return audio_content, tmp_file.name

def clone_voice(audio_path: str, target_voice_path: str, output_dir: str = "output") -> str:
    """
    Clone the voice of the input audio to match the target voice sample.

    Args:
        audio_path (str): Path to the input audio file to be cloned.
        target_voice_path (str): Path to the target voice sample audio file.
        output_dir (str): Directory to save the cloned audio file. Default is "output". 
    Returns:
        str: The path to the cloned audio file in WAV format.
    """
    cloned_audio = cloning_model.generate(
        audio=audio_path, target_voice_path=target_voice_path,
    )

    # Save the cloned audio
    # Create output_dir if not exists
    os.makedirs(output_dir, exist_ok=True)
    audio_filepath = os.path.join(output_dir, "cloned_output.wav")
    ta.save(audio_filepath, cloned_audio, cloning_model.sr)

    return audio_filepath

if __name__ == "__main__":
    text = "Halo, nama saya Dira Yuanita. Suara ini dihasilkan oleh model text-to-speech Chirp 3 dari Google Cloud."
    audio_content, tmp_filepath = generate_speech(text, voice="Leda", language_code="id-ID")
    with open("output/tmp.mp3", "wb") as out:
        out.write(audio_content)
    print("Audio content written to file 'tmp.mp3'")


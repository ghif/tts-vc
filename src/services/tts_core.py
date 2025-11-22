# Check if this code is inside google colab environment
try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

import os
import time
import threading

from dotenv import load_dotenv
load_dotenv()

from google.cloud import texttospeech_v1beta1 as texttospeech
from google.api_core.client_options import ClientOptions

import tempfile

from vc import VoiceCloner
import torch
import torchaudio as ta
from torch.amp import autocast

def get_safe_device():
    """
    Get the safest device for large model inference.
    """
    if torch.cuda.is_available():
        device = "cuda"
        print(f"Using CUDA: {torch.cuda.get_device_name()}")
    elif torch.backends.mps.is_available():
        # MPS has memory limitations with large models, use CPU instead
        print("MPS available but using CPU for large model stability")
        device = "cpu"
        # device = "mps"
    else:
        device = "cpu"
        print("Using CPU")
    
    return device

DEVICE = get_safe_device()
    
# Load voice cloning model
cloning_model = VoiceCloner.from_pretrained(DEVICE)


if IN_COLAB:
    from google.colab import userdata
    PROJECT_ID = userdata.get("PROJECT_ID")
    TTS_LOCATION = userdata.get("TTS_LOCATION")

else:
    PROJECT_ID = os.getenv("PROJECT_ID")
    TTS_LOCATION = os.getenv("TTS_LOCATION")

API_ENDPOINT = (
    f"{TTS_LOCATION}-texttospeech.googleapis.com"
    if TTS_LOCATION != "global"
    else "texttospeech.googleapis.com"
)

def schedule_cleanup(filepath: str, delay_seconds: int = 1800):
    """
    Schedule file cleanup after some seconds.
    """
    def cleanup():
        time.sleep(delay_seconds)
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
                print(f"Cleaned up temporary file: {filepath}")
        except Exception as e:
            print(f"Error cleaning up file {filepath}: {e}")
    
    threading.Thread(target=cleanup, daemon=True).start()

def list_voices():
    """
    List the available voices.
    """
    client = texttospeech.TextToSpeechClient(
        client_options=ClientOptions(api_endpoint=API_ENDPOINT)
    )
    response = client.list_voices()
    return response.voices

def generate_speech(text, voice="Leda", language_code="id-ID"):
    """
    Generate speech using Google's Chirp 3 Text-to-Speech API

    Args:
        text (str): The text to be synthesized.
        voice (str): The name of the voice to use (e.g., "Leda", "Charon").
        language_code (str): The language code for the voice (e.g., "id-ID" for Indonesian, "en-US" for English).
    Returns:
        audio_content (bytes): The synthesized speech audio in MP3 format.
        temporary_file_name (str): The filename of the synthesized audio.
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
            # audio_encoding=texttospeech.AudioEncoding.MP3
            audio_encoding=texttospeech.AudioEncoding.MP3
        ),
    )

    # Create a temporary MP3 file
    audio_content = response.audio_content

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_content)
    
    schedule_cleanup(tmp_file.name)
    return audio_content, tmp_file.name

def clone_voice(audio_path: str, target_voice_path: str) -> str:
    """
    Clone the voice of the input audio to match the target voice sample.

    Args:
        audio_path (str): Path to the input audio file to be cloned.
        target_voice_path (str): Path to the target voice sample audio file.
        output_dir (str): Directory to save the cloned audio file. Default is "output". 
    Returns:
        str: The path to the cloned audio file in WAV format.
    """
    with torch.inference_mode():
        if DEVICE == "cuda":
            with autocast(device_type=DEVICE, dtype=torch.float16):
                cloned_audio = cloning_model.generate(
                    audio=audio_path, target_voice_path=target_voice_path,
                )
        else:
            cloned_audio = cloning_model.generate(
                audio=audio_path, target_voice_path=target_voice_path,
            )

    # Save the cloned audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        ta.save(tmp_wav.name, cloned_audio, cloning_model.sr)
    
    schedule_cleanup(tmp_wav.name)

    return tmp_wav.name
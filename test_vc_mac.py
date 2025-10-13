import torch
import torchaudio as ta

from vc import VoiceCloner

import os

# Automatically detect the best available device
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using device: {device}")

# Paths to the input audio and target voice sample
AUDIO_PATH = "resources/tts_id-ID-Chirp3-HD-Charon.mp3"
# TARGET_VOICE_PATH = "resources/ghif_reference_EN.wav"
TARGET_VOICE_PATH = "resources/ghif_reference_ID.wav"

# Get filename from AUDIO_PATH and TARGET_VOICE_PATH
audio_filename = os.path.splitext(os.path.basename(AUDIO_PATH))[0]
target_voice_filename = os.path.splitext(os.path.basename(TARGET_VOICE_PATH))[0]

# Clone the voice
model = VoiceCloner.from_pretrained(device)
wav = model.generate(
    audio=AUDIO_PATH,
    target_voice_path=TARGET_VOICE_PATH,
)

# Save the cloned audio
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
ta.save(f"{output_dir}/cloned_{audio_filename}_{target_voice_filename}.wav", wav, model.sr)
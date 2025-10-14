# TTS-VC: Text-to-Speech and Voice Cloning

A simple Python implementation for text-to-speech synthesis and voice cloning using state-of-the-art models including Chirp 3 and CosyVoice. This is used for an educational material.


## Features

- **Text-to-Speech**: Generate natural-sounding speech from text using Chirp 3
- **Voice Cloning**: Clone voices using advanced neural models from CosyVoice
- **UI Prototype**: Simple UI prototype with Gradio

## Installation

### Requirements

The detailed requirements can be found in pyproject.toml. It was specified such that it can be easily run on Google Colab.

- Python >= 3.12.11
- PyTorch >= 2.8.0
- Chirp 3 HD API

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/ghif/tts-vc.git
cd tts-vc
```

2. Install in development mode:
```bash
# conda create -yn tts-vc python=3.12.11
# conda activate tts-vc
pip install -e .
```

### Google Cloud Setup (Optional)

For Google Cloud TTS features:

1. Install Google Cloud SDK
2. Set up authentication:
```bash
gcloud auth application-default login
```
3. Enable the Text-to-Speech API in your Google Cloud Console
4. Set the environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

## Quick Start

### Basic Voice Cloning

```python
from src import VoiceCloner
import torch
import torchaudio

# Initialize the voice cloner
vc = VoiceCloner()

# Load reference audio for voice cloning
reference_audio, sr = torchaudio.load("reference_voice.wav")

# Clone voice with new text
cloned_audio = vc.clone_voice(
    text="Hello, this is a cloned voice!",
    reference_audio=reference_audio,
    sample_rate=sr
)

# Save the result
torchaudio.save("cloned_output.wav", cloned_audio, sr)
```

### Text-to-Speech

```python
from tts_services import GoogleTTSService

# Initialize TTS service
tts = GoogleTTSService()

# Generate speech
audio_data = tts.synthesize(
    text="Hello, world!",
    voice_name="en-US-Neural2-F"
)

# Save audio
with open("output.wav", "wb") as f:
    f.write(audio_data)
```


## Models

### Supported Models

- **CosyVoice**: Advanced voice cloning with natural prosody
- **Chirp 3**: State-of-the-art speech synthesis
- **Google Cloud TTS**: Cloud-based text-to-speech with multiple voices
- **S3 Tokenizer**: Advanced tokenization for speech processing

### Model Features

- English and Indonesian languages support
- Real-time inference
- High-quality audio synthesis
- Voice adaptation and cloning

## Configuration

### Environment Variables

```bash
# Google Cloud TTS (optional)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# Model paths (if using local models)
export MODEL_PATH="path/to/models"
```

### Dependencies

Core dependencies include:
- PyTorch 2.8.0
- Transformers 4.57.0
- Librosa 0.11.0
- Diffusers 0.35.1
- NumPy >= 2.0.2

## Usage Examples

### Advanced Voice Cloning


## API Reference

### VoiceCloner Class

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

## Development Setup

```bash
# Clone repository
git clone https://github.com/ghif/tts-vc.git
cd tts-vc

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
python test_vc_mac.py
```

## Troubleshooting

### Common Issues

1. **ImportError: attempted relative import with no known parent package**
   ```bash
   pip install -e .  # Install package properly
   ```

2. **CUDA out of memory**
   ```python
   # Use CPU or reduce batch size
   vc = VoiceCloner(device="cpu")
   ```

3. **Google Cloud authentication errors**
   ```bash
   gcloud auth application-default login
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
   ```

## License

This project is licensed under the terms specified in the LICENSE file.


## Acknowledgments

- Resemble AI team for the neat code implementation of the voice cloning in [Chatterbox](https://github.com/resemble-ai/chatterbox).
- [CosyVoice](https://funaudiollm.github.io/cosyvoice2/) team for the voice cloning model
- Google for [Chirp 3](https://cloud.google.com/text-to-speech/docs/chirp3-hd) TTS services
- [PyTorch](https://pytorch.org/) team for the deep learning framework
- [Transformers](https://huggingface.co/docs/transformers/en/index) library by Hugging Face

## Contact

- Email: mghifary@gmail.com
- GitHub: [https://github.com/ghif/tts-vc](https://github.com/ghif/tts-vc)
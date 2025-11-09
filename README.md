# TTS-VC: Text-to-Speech and Voice Cloning

A simple Python implementation for text-to-speech synthesis and voice cloning using state-of-the-art models including Chirp 3 and Chatterbox. This is used for an educational material.


## Features

- **Text-to-Speech**: Generate natural-sounding speech from text using Chirp 3
- **Voice Cloning**: Clone voices using advanced neural models from Chatterbox
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

### Text-to-Speech

```python
import services.tts_core as tts

# Generate speech with Chirp 3 TTS
voice = "Charon"
language_code = "id-ID"
tts_audio, tts_filepath = tts.generate_speech(text, voice=voice, language_code=language_code)
```


### Basic Voice Cloning

```python
import services.tts_core as tts

# Paths to the input audio and target voice sample
AUDIO_PATH = "<PATH TO SOURCE AUDIO (wav/mp3)>"
TARGET_VOICE_PATH = "<PATH TO REFERENCE AUDIO (wav/mp3)>"

cloned_filepath = tts.clone_voice(AUDIO_PATH, TARGET_VOICE_PATH)
```


## Models

### Supported Models

- **Chatterbox**: 
- **CosyVoice**: Advanced voice cloning with natural prosody, including the S3 tokenizer
- **Chirp 3**: State-of-the-art speech synthesis
- **Google Cloud TTS**: Cloud-based text-to-speech with multiple voices

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
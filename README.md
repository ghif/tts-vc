# TTS-VC: Text-to-Speech and Voice Cloning

A simple Python implementation for text-to-speech synthesis and voice cloning using state-of-the-art models including Chirp 3 and Chatterbox. This is used for an educational material.

## Features

- **Text-to-Speech**: Generate natural-sounding speech from text using Chirp 3
- **Voice Cloning**: Clone voices using advanced neural models from Chatterbox
- **UI Prototype**: Simple UI prototype with Gradio

## Project Structure

```
├── app.py                  # Gradio application for online demo
├── Dockerfile              # Dockerfile for containerization
├── LICENSE                 # Project license
├── pyproject.toml          # Project dependencies and metadata
├── README.md               # This README file
├── resources/              # Sample audio and text files
├── src/                    # Source code
│   ├── services/           # Core services for TTS and voice cloning
│   │   └── tts_core.py
│   └── models/             # Voice cloning models
└── test_vc_mac.py          # Test script for voice cloning
```

## Installation

### Requirements

The detailed requirements can be found in pyproject.toml. It was specified such that it can be easily run on Google Colab.

- Python >= 3.12.11
- PyTorch >= 2.8.0
- Chirp 3 HD API


### Run on Google Colab
To run this repository on Google Colab, see the following notebook script:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/15YdikRcUDuAKxOdiYja468Ughj_oE-X9?usp=sharing)

### Run on Local Machine

1. Clone the repository:
```bash
git clone https://github.com/ghif/tts-vc.git
cd tts-vc
```

2. Install in development mode:
```bash
conda create -yn tts-vc python=3.12.11
conda activate tts-vc
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

## Usage

### Gradio Interface

To run the Gradio interface, you can run `app.py`:

```bash
python app.py
```

### Quick Start

#### Text-to-Speech

```python
import services.tts_core as tts

# Generate speech with Chirp 3 TTS
voice = "Charon"
language_code = "id-ID"
tts_audio, tts_filepath = tts.generate_speech(text, voice=voice, language_code=language_code)
```


#### Basic Voice Cloning

```python
import services.tts_core as tts

# Paths to the input audio and target voice sample
AUDIO_PATH = "<PATH TO SOURCE AUDIO (wav/mp3)>"
TARGET_VOICE_PATH = "<PATH TO REFERENCE AUDIO (wav/mp3)>"

cloned_filepath = tts.clone_voice(AUDIO_PATH, TARGET_VOICE_PATH)
```

## API Reference

### `services.tts_core.generate_speech(text, voice="Leda", language_code="id-ID")`

- **text** (str): The text to be synthesized.
- **voice** (str, optional): The name of the voice to use (e.g., "Leda", "Charon"). Defaults to "Leda".
- **language_code** (str, optional): The language code for the voice (e.g., "id-ID" for Indonesian, "en-US" for English). Defaults to "id-ID".

**Returns**: A tuple containing the audio content in bytes and the path to the temporary audio file.

### `services.tts_core.clone_voice(audio_path, target_voice_path)`

- **audio_path** (str): Path to the input audio file to be cloned.
- **target_voice_path** (str): Path to the target voice sample audio file.

**Returns**: The path to the cloned audio file in WAV format.

## Testing

To run the test script for voice cloning, run the following command:

```bash
python test_vc_mac.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Models

### Supported Models

- **Chatterbox**: Production-grade open-source TTS model supporting 23 languages.
- **CosyVoice**: Advanced voice cloning with natural prosody, including the S3 tokenizer.
- **Chirp 3**: Latest generation of TTS technology from Google.

### Model Features

- English and Indonesian languages support
- Real-time inference
- High-quality audio synthesis
- Voice adaptation and cloning

## Configuration

### Environment Variables

To configure environment variables, copy the `.env.sample` file to `.env` and adjust the values:

```bash
cp .env.sample .env
# Open .env and set your PROJECT_ID and TTS_LOCATION
```

Example `.env` file:
```
PROJECT_ID="your-gcp-project-id"
TTS_LOCATION="global"
```

Additionally, for Google Cloud TTS features:

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

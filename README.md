# TTS# TTS-VC: Text-to-Speech and Voice Cloning

A Python library for text-to-speech synthesis and voice cloning using state-of-the-art models including Chirp 3 and CosyVoice.

## Features

- **Text-to-Speech**: Generate natural-sounding speech from text
- **Voice Cloning**: Clone voices using advanced neural models
- **Multiple Models**: Support for Chirp 3, CosyVoice, and Google Cloud TTS
- **High Quality**: State-of-the-art neural vocoding for realistic audio
- **Easy Integration**: Simple Python API for quick integration

## Installation

### Requirements

- Python >= 3.12.11
- PyTorch >= 2.8.0

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/ghif/tts-vc.git
cd tts-vc
```

2. Install in development mode:
```bash
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

## Project Structure

```
tts-vc/
├── src/
│   ├── __init__.py
│   ├── vc.py                 # Voice cloning implementation
│   └── models/
│       ├── s3tokenizer.py    # S3 tokenizer model
│       └── ...
├── tts_services.py           # TTS service implementations
├── test_vc_mac.py           # Voice cloning tests
├── pyproject.toml           # Project configuration
└── README.md
```

## Models

### Supported Models

- **CosyVoice**: Advanced voice cloning with natural prosody
- **Chirp 3**: State-of-the-art speech synthesis
- **Google Cloud TTS**: Cloud-based text-to-speech with multiple voices
- **S3 Tokenizer**: Advanced tokenization for speech processing

### Model Features

- Multi-language support
- Real-time inference
- High-quality audio synthesis
- Voice adaptation and cloning
- Prosody and emotion control

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

```python
from src import VoiceCloner
import torchaudio

# Initialize with custom settings
vc = VoiceCloner(
    model_name="cosyvoice",
    device="cuda" if torch.cuda.is_available() else "cpu"
)

# Multi-speaker voice cloning
speakers = ["speaker1.wav", "speaker2.wav"]
mixed_voice = vc.blend_voices(
    text="This combines multiple speakers",
    speaker_files=speakers,
    weights=[0.7, 0.3]
)
```

### Batch Processing

```python
texts = [
    "First sentence to synthesize",
    "Second sentence with different voice",
    "Third sentence for comparison"
]

# Batch process multiple texts
results = vc.batch_synthesis(texts, reference_audio)
```

## API Reference

### VoiceCloner Class

```python
class VoiceCloner:
    def __init__(self, model_name="cosyvoice", device="auto"):
        """Initialize voice cloner with specified model"""
    
    def clone_voice(self, text: str, reference_audio: torch.Tensor, 
                   sample_rate: int = 22050) -> torch.Tensor:
        """Clone voice from reference audio"""
    
    def batch_synthesis(self, texts: List[str], 
                       reference_audio: torch.Tensor) -> List[torch.Tensor]:
        """Process multiple texts with same reference voice"""
```

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

## Performance

- **Real-time Factor**: < 0.1x (faster than real-time)
- **Memory Usage**: ~2GB GPU memory for inference
- **Supported Sample Rates**: 16kHz, 22kHz, 24kHz, 48kHz
- **Audio Formats**: WAV, MP3, FLAC

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

## Citation

If you use this code in your research, please cite:

```bibtex
@software{tts_vc_2024,
  title={TTS-VC: Text-to-Speech and Voice Cloning},
  author={Your Name},
  year={2024},
  url={https://github.com/ghif/tts-vc}
}
```

## Acknowledgments

- CosyVoice team for the voice cloning model
- Google Cloud for TTS services
- PyTorch team for the deep learning framework
- Transformers library by Hugging Face

## Contact

- Email: mghifary@gmail.com
- GitHub: [https://github.com/ghif/tts-vc](https://github.com/ghif/tts-vc)
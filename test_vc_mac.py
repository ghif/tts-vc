import sys
sys.path.append("src")

import services.tts_core as tts


def test_clone_voice():
    """
    Test the voice cloning functionality.
    """
    # Paths to the input audio and target voice sample
    AUDIO_PATH = "resources/samples/LJ025-0076.wav"
    TARGET_VOICE_PATH = "resources/ref_speech.wav"

    cloned_filepath = tts.clone_voice(AUDIO_PATH, TARGET_VOICE_PATH)

    print(f"Cloned audio saved at: {cloned_filepath}")


if __name__ == "__main__":
    test_clone_voice()
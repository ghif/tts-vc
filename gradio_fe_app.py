"""
Gradio frontend for text-to-speech synthesis.
Use tts_google.py for Google Chirp 3 TTS integration.
"""

import gradio as gr
import tempfile

import services.tts_core as tts


def synthesize_speech(text_filepath: str, voice: str = "Leda", language_code: str = "id-ID", ref_audio: str="resources/ghif_reference_ID.wav") -> str:
    """
    Synthesize speech using Google Chirp 3 TTS and return the path to the audio file.
    Args:
        text (str): The text to be synthesized.
        voice (str): The name of the voice to use (e.g., "Leda", "Charon").
        language_code (str): The language code for the voice (e.g., "id-ID" for Indonesian, "en-US" for English).
    Returns:
        str: The path to the synthesized audio file in MP3 format.
    """
    print(f"Text file: {text_filepath}, Voice: {voice}, Language Code: {language_code}, Ref Audio: {ref_audio}")

    # Read text from uploaded file
    if text_filepath is None:
        return None, None

    with open(text_filepath, "r") as f:
        text = f.read().strip()
    
    if not text:
        return None, None

    # Generate speech with Chirp 3 TTS
    tts_audio, tts_filepath = tts.generate_speech(text, voice=voice, language_code=language_code)

    cloned_filepath = tts.clone_voice(tts_filepath, ref_audio)

    return tts_filepath, cloned_filepath

with gr.Blocks(
    title="Text-to-Speech (TTS) and Voice Cloning with Chirp 3 and CosyVoice",
    theme=gr.themes.Soft(),
    css="""
    .main-container {max-width: 800px; margin: 0 auto; }
    .header { text-align: center; margin-bottom: 2rem;}
    """
) as demo:
    gr.HTML("""
        <div class="header">
            <h1>🎙️ Generate and Clone Your Own Voice</h1>
            <p>Convert text to natural-sounding speech using Google's Chirp 3 and CosyVoice</p>
        </div>
        """)

    with gr.Row():
        with gr.Column():
            text_file = gr.File(
                label="Upload Text File (.txt)",
                file_types=[".txt"],
                type="filepath"
            )
            
            voice = gr.Dropdown(choices=["Charon", "Leda"], value="Charon", label="Chirp 3's Voice Character")
            language_code = gr.Dropdown(choices=["id-ID", "en-US"], value="id-ID", label="Language Code")
            ref_audio = gr.Audio(sources=["upload", "microphone"], interactive=True, label="Reference Voice Sample (Target Voice)", type="filepath", value="resources/ghif_reference_ID.mp3")
            run_btn = gr.Button("Generate", variant="primary")

        with gr.Column():
            audio_tts_output = gr.Audio(label="Original TTS Audio Output", show_download_button=True, type="filepath")
            audio_vc_output = gr.Audio(label="Cloned Audio Output", show_download_button=True, type="filepath")


    run_btn.click(
        fn=synthesize_speech,
        inputs=[
            text_file,
            voice,
            language_code,
            ref_audio,
        ],
        # outputs=audio_output,
        outputs=[audio_tts_output, audio_vc_output],
    )

if __name__ == "__main__":
    # demo.queue(
    #     max_size=50,
    #     default_concurrency_limit=1,
    # ).launch(share=True)
    demo.queue(
        max_size=50,
        default_concurrency_limit=1,
    ).launch()
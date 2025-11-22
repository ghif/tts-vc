"""
Gradio frontend for text-to-speech synthesis.
Use tts_google.py for Google Chirp 3 TTS integration.
"""

import sys
import os

# Add 'src' to sys.path to ensure modules can be imported
sys.path.append(os.path.abspath("src"))

import gradio as gr
import services.tts_core as tts


def synthesize_speech(input_method: str, text_input: str, text_filepath: str, voice: str = "Leda", language_code: str = "id-ID", ref_audio: str="resources/ghif_reference_ID.wav") -> str:
    """
    Synthesize speech using Google Chirp 3 TTS and return the path to the audio file.
    Args:
        text (str): The text to be synthesized.
        voice (str): The name of the voice to use (e.g., "Leda", "Charon").
        language_code (str): The language code for the voice (e.g., "id-ID" for Indonesian, "en-US" for English).
    Returns:
        str: The path to the synthesized audio file in MP3 format.
    """
    if input_method == "Text Input":
        text = text_input
    else: # File Upload
        # Read text from uploaded file
        if text_filepath is None:
            return None, None

        with open(text_filepath, "r") as f:
            text = f.read()
    
    text = text.strip()
    if len(text) == 0:
        return None, None

    # Generate speech with Chirp 3 TTS
    tts_audio, tts_filepath = tts.generate_speech(text, voice=voice, language_code=language_code)

    cloned_filepath = tts.clone_voice(tts_filepath, ref_audio)

    return tts_filepath, cloned_filepath


# Function to toggle input method visibility
def toggle_input_method(method: str):
    if method == "Text Input":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)
    
with gr.Blocks(
    title="Text-to-Speech (TTS) and Voice Cloning with Chirp 3 and Resemble AI",
    theme=gr.themes.Soft(),
    css="""
    .main-container {max-width: 800px; margin: 0 auto; }
    .header { text-align: center; margin-bottom: 2rem;}
    .footer { text-align: center; margin-top: 2rem; }
    """
) as demo:
    gr.HTML("""
        <div class="header">
            <h1>🎙️ Generate and Clone Your Own Voice</h1>
            <p>
            Convert text to natural-sounding speech using Google's <a href="https://cloud.google.com/text-to-speech/docs/chirp3-hd">Chirp 3: HD Voices</a> and Resemble AI's  <a href="https://github.com/resemble-ai/chatterbox">Chatterbox</a>.
            </p>
            <p>
            All the audio input and generated files are not permanent and will be deleted after a short period of time.
            </p>
        </div>
        """)

    with gr.Row():
        with gr.Column():
            # Radio button to choose input method
            input_method = gr.Radio(
                choices=["Text Input", "File Upload"],
                value="Text Input",
                label="Choose Input Method",
            )
            # Text input box
            text_input = gr.Textbox(
                label="Enter Text to Synthesize",
                interactive=True,
                lines=5,
                value="Halo semuanya. Selamat datang di demo text-to-speech menggunakan Google Chirp 3 dan voice cloning menggunakan Chatterbox. Silakan coba dengan teks buatanmu sendiri!"
            )

            # File upload for text file
            text_file = gr.File(
                label="Upload Text File (.txt)",
                file_types=[".txt"],
                type="filepath",
                visible=False,

            )
            
            voice = gr.Dropdown(choices=["Charon", "Leda"], value="Charon", label="Chirp 3's Voice Character")
            language_code = gr.Dropdown(choices=["id-ID", "en-US"], value="id-ID", label="Language Code")
            ref_audio = gr.Audio(sources=["upload", "microphone"], interactive=True, label="Reference Voice Sample (Target Voice)", show_download_button=True, type="filepath", value="resources/samples/LJ025-0076.wav")
            run_btn = gr.Button("Generate", variant="primary")

        with gr.Column():
            audio_tts_output = gr.Audio(label="Original TTS Audio Output", show_download_button=True, type="filepath")
            audio_vc_output = gr.Audio(label="Cloned Audio Output", show_download_button=True, type="filepath")


    # Change event for input method radio button
    input_method.change(
        fn=toggle_input_method,
        inputs=input_method,
        outputs=[text_input, text_file],
    )

    # Click event for the run button
    run_btn.click(
        fn=synthesize_speech,
        inputs=[
            input_method,
            text_input,
            text_file,
            voice,
            language_code,
            ref_audio,
        ],
        outputs=[audio_tts_output, audio_vc_output],
    )

    gr.HTML("""
        <div class="footer">
            <p>
            Powered by <a href="https://cloud.google.com/text-to-speech/docs/chirp3-hd">Google Chirp 3</a> and <a href="https://github.com/resemble-ai/chatterbox">Chatterbox</a>.
            </p>
        </div>
        """)

if __name__ == "__main__":
    # demo.queue(
    #     max_size=50,
    #     default_concurrency_limit=1,
    # ).launch(share=True)
    demo.launch()

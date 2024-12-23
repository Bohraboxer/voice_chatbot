import streamlit as st
from audio_recorder_streamlit import audio_recorder
from pathlib import Path

def record_audio():
    """Record audio using Streamlit widget."""
    st.write("Press the button below to record your query.")
    audio_bytes = audio_recorder(pause_threshold=1.2, sample_rate=16000)

    if audio_bytes:
        output_dir = Path("recordings")
        output_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist
        output_file = output_dir / "recorded_audio.wav"

        with open(output_file, "wb") as f:
            f.write(audio_bytes)

        return str(output_file)

    return None
from deepgram import DeepgramClient, FileSource, PrerecordedOptions
import streamlit as st
import os
from dotenv import load_dotenv


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
def transcribe_audio(audio_file_path):
    """Transcribe audio using Deepgram API."""
    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        with open(audio_file_path, "rb") as audio_file:
            payload = {"buffer": audio_file.read(), "mimetype": "audio/wav"}
        options = PrerecordedOptions(model="nova-2", language="en-IN", smart_format=True)
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        transcript = response.results.channels[0].alternatives[0].transcript
        return transcript
    except Exception as e:
        st.error(f"Error in transcription: {e}")
        return None

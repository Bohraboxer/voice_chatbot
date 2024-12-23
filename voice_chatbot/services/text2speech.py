import tempfile
from deepgram import DeepgramClient, SpeakOptions
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def generate_tts(text, audio_filename):
    """Generate text-to-speech audio using Deepgram API."""
    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        options = SpeakOptions(model="aura-orion-en")
        response = deepgram.speak.v("1").save(audio_filename, {"text": text}, options)
        return audio_filename
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

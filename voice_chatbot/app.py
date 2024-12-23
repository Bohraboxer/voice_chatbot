
import streamlit as st
from services.recorder import record_audio
from services.transcription import transcribe_audio
from services.llm_integration import stream_llm_response
from services.text2speech import generate_tts
import asyncio
import os
from pydub import AudioSegment  # For calculating audio duration
import time

# Streamlit app configuration
st.set_page_config(page_title="Voice Query Chatbot", page_icon="🎤")

# App title
st.title("🎤 Voice Query Chatbot")

# Initialize conversation history in Streamlit session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Step 1: Record audio
st.header("Step 1: Record Your Query")
audio_file_path = record_audio()

# Create a temporary directory to store generated audio files
temp_audio_dir = "temp_audio"
os.makedirs(temp_audio_dir, exist_ok=True)

# Function to get the duration of an audio file
def get_audio_duration(audio_path):
    """Calculate the duration of the given audio file."""
    audio = AudioSegment.from_mp3(audio_path)
    return audio.duration_seconds  # Duration in seconds

# Function to play audio and wait for completion
def play_audio_with_full_duration(audio_path, duration):
    """
    Play the audio file in the Streamlit player and wait for the duration.
    Args:
        audio_path (str): Path to the audio file.
        duration (float): Duration of the audio file in seconds.
    """
    st.audio(audio_path, format="audio/mp3", start_time=0, autoplay=True)
    time.sleep(duration)  # Ensure full playback time

# Function to format conversation history for LLM
def format_conversation_for_llm(conversation):
    """Format conversation history into a prompt for the LLM."""
    formatted_prompt = ""
    for exchange in conversation:
        if exchange['role'] == 'user':
            formatted_prompt += f"User: {exchange['content']}\n"
        else:
            # Avoid duplicating "Assistant:" prefix in the LLM response
            response = exchange['content'].replace("Assistant: ", "").strip()
            formatted_prompt += f"Assistant: {response}\n"
    return formatted_prompt

# Async function to process audio, transcribe, and play generated TTS
async def process_audio(audio_file_path):
    st.header("Step 2: Transcribe Query")
    with st.spinner("Transcribing..."):
        # Transcribe the audio file asynchronously
        user_query = await asyncio.to_thread(transcribe_audio, audio_file_path)

    if user_query:
        st.success("Transcription Complete!")
        st.write(f"**Your Query:** {user_query}")

        # Add user query to conversation
        st.session_state.conversation.append({"role": "user", "content": user_query})

        # Format conversation history for LLM
        conversation_context = format_conversation_for_llm(st.session_state.conversation)

        st.header("Step 3: Streaming Response")
        with st.spinner("Processing your query..."):
            try:
                sentence_buffer = ""
                sentence_count = 0

                # Stream LLM response
                async for chunk in stream_llm_response(conversation_context):
                    if chunk.strip():
                        sentence_buffer += chunk

                        # Process complete sentences
                        if sentence_buffer.endswith(('.', '!', '?')):
                            sentence_count += 1
                            audio_filename = f"{temp_audio_dir}/sentence_{sentence_count}.mp3"
                            audio_response_path = await asyncio.to_thread(generate_tts, sentence_buffer, audio_filename)

                            if audio_response_path:
                                audio_duration = get_audio_duration(audio_response_path)
                                play_audio_with_full_duration(audio_response_path, audio_duration)

                                # Append assistant response to conversation
                                st.session_state.conversation.append({"role": "assistant", "content": sentence_buffer.strip()})

                                # Reset buffer
                                sentence_buffer = ""
                            else:
                                st.warning("Failed to generate audio for this chunk.")
            except Exception as e:
                st.error(f"Error streaming response: {e}")

        # Display conversation history
        st.header("Conversation History")
        for exchange in st.session_state.conversation:
            if exchange['role'] == 'user':
                st.write(f"**User:** {exchange['content']}")
            else:
                st.write(f"**Assistant:** {exchange['content']}")
    else:
        st.warning("Could not transcribe the audio. Please try again.")

# Execute the process if audio is recorded
if audio_file_path:
    asyncio.run(process_audio(audio_file_path))

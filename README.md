# Voice Query Chatbot

## Overview
The Voice Query Chatbot is a Streamlit-based application that allows users to interact with a chatbot using voice input. The application records audio queries, transcribes them into text, generates responses using an LLM (Language Learning Model), and converts the responses back to speech for playback. This facilitates seamless, voice-based conversational interactions.

## Features
- **Audio Recording:** Users can record their voice queries directly within the app.
- **Audio Transcription:** Converts recorded audio into text using Deepgram's transcription services.
- **Conversational AI:** Integrates with OpenAI's GPT-3.5-turbo model to generate intelligent responses.
- **Text-to-Speech Conversion:** Uses Deepgram's text-to-speech (TTS) to convert LLM responses into audio for playback.
- **Session Management:** Maintains conversation history throughout the session.

## File Structure
```
voice_chatbot/
├── app.py                 # Main application file
├── services/
│   ├── init.py        
│   ├── recorder.py        # Handles audio recording
│   ├── transcription.py   # Manages audio-to-text transcription
│   ├── llm_integration.py # Manages interaction with the LLM
│   ├── text2speech.py     # Handles text-to-speech conversion
├── recordings/            # Directory to store recorded audio
├── temp_audio/            # Temporary directory for generated audio files
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bohraboxer/voice_chatbot.git
   cd voice_chatbot
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file Add your API keys:
   - Update `DEEPGRAM_API_KEY` in .env with your Deepgram API key.
   - Update `openai.api_key` in .env with your OpenAI API key.

## Usage

1. Run the application:
   ```bash
   streamlit run voice_chatbot/app.py
   ```

2. Open the app in your web browser at `http://localhost:8501`.

3. Follow these steps in the app:
   - **Step 1:** Record your query using the microphone button.
   - **Step 2:** View the transcribed text of your query.
   - **Step 3:** Listen to the chatbot's audio response.
   - Review the conversation history displayed on the app.

## Dependencies
- **Streamlit:** For building the web interface.
- **Pydub:** For calculating audio file duration.
- **Deepgram SDK:** For transcription and text-to-speech.
- **OpenAI API:** For LLM integration.

## API Key Setup
Ensure that you have valid API keys for:
- **Deepgram:** Used for transcription and text-to-speech.
- **OpenAI:** Used for generating chatbot responses.

## Key Components

### `app.py`
- Handles the overall application workflow, including user interface, conversation management, and integration of various services.

### `recorder.py`
- Provides functionality to record audio input from the user and save it locally.

### `transcription.py`
- Manages audio-to-text conversion using Deepgram's transcription services.

### `llm_integration.py`
- Facilitates interaction with OpenAI's GPT-3.5-turbo model, streaming responses to the user.

### `text2speech.py`
- Converts the chatbot's text responses into speech audio files using Deepgram's TTS service.

## Troubleshooting
- **Audio not recording:** Ensure your microphone permissions are enabled for the browser.
- **Transcription errors:** Verify that the audio file is correctly recorded and the Deepgram API key is valid.
- **No response from chatbot:** Confirm the OpenAI API key is correctly set up.
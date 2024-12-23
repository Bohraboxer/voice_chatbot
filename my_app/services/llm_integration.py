# llm_integration.py
import openai
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def stream_llm_response(user_query):
    """Stream response from OpenAI's GPT model."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_query}],
            stream=True,
        )
        for chunk in response:
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0]["delta"]
                if "content" in delta:
                    yield delta["content"]
    except Exception as e:
        yield f"Error streaming response: {e}"
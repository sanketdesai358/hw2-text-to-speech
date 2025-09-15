from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate audio and save as mp3
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input="Hello, this is my test for text-to-speech."
) as response:
    response.stream_to_file("hello.mp3")

print("Audio file saved as hello.mp3")

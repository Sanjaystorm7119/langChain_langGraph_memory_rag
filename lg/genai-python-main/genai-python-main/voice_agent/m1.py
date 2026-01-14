import asyncio
import os
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

# Configure Gemini for text generation
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Use latest Gemini model

# Use OpenAI for TTS
async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input=speech,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        conversation_history = []

        while True:
            try:
                print("Speak Something...")
                audio = r.listen(source)

                print("Processing Audio... (STT)")
                stt = r.recognize_google(audio)
                print("You Said:", stt)

                # Build context from conversation history
                context = "\n".join(conversation_history[-10:])  # Last 10 exchanges
                
                prompt = f"""
                    You're a cheerful voice assistant. Respond naturally and keep it concise for voice interaction.

Previous conversation:
{context}

User: {stt}

Respond as a helpful, upbeat assistant:"""

                response = model.generate_content(prompt)
                ai_response = response.text

                print("AI Response:", ai_response)
                
                # Update conversation history
                conversation_history.append(f"User: {stt}")
                conversation_history.append(f"Assistant: {ai_response}")
                
                asyncio.run(tts(speech=ai_response))

            except sr.UnknownValueError:
                print("Could not understand audio")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
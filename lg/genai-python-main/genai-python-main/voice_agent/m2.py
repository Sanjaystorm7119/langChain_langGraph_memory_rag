import os
from dotenv import load_dotenv
import speech_recognition as sr
import google.generativeai as genai
from google.cloud import texttospeech
import pygame
import io
import tempfile

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')
tts_client = texttospeech.TextToSpeechClient()

def tts(speech: str):
    synthesis_input = texttospeech.SynthesisInput(text=speech)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-F",  # Natural sounding voice
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.1,  # Slightly faster for natural conversation
        pitch=2.0,  # Slightly higher pitch for cheerful tone
    )
    
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # Play audio using pygame
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tmp_file.write(response.audio_content)
        tmp_file.flush()
        
        pygame.mixer.init()
        pygame.mixer.music.load(tmp_file.name)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    
    os.unlink(tmp_file.name)  # Clean up temp file
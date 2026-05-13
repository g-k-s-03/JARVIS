import sounddevice as sd
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write
import os

def listen():
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording
    
    print("JARVIS is listening (5 seconds)...")
    
    # Record audio
    myrecording = sd.rec(seconds * fs, samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    
    # Save as temporary wav file
    write('output.wav', fs, myrecording)
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile('output.wav') as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)  # type: ignore[attr-defined]
            print(f"You said: {text}")
            return text.lower()
    except Exception as e:
        print("I didn't catch that.")
        return None
    finally:
        if os.path.exists('output.wav'):
            os.remove('output.wav')

if __name__ == "__main__":
    listen()
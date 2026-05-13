import pyttsx3

# Initialize engine globally to prevent "run loop already started" errors
engine = pyttsx3.init()
# You can adjust rate (speed) and volume here
engine.setProperty('rate', 175) 

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass

if __name__ == "__main__":
    speak("Systems online. I am JARVIS, your cybersecurity assistant.")
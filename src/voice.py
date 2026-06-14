import pyttsx3

# Initialised once at module level to avoid "run loop already started" resource leaks
engine = pyttsx3.init()
engine.setProperty('rate', 175)


def speak(text: str) -> None:
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS WARNING]: Could not speak response: {e}")


if __name__ == "__main__":
    speak("Systems online. I am JARVIS, your cybersecurity assistant.")

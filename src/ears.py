import speech_recognition as sr
from typing import Optional


def listen() -> Optional[str]:
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("JARVIS is listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return None
    except OSError as e:
        print(f"[EARS ERROR]: Microphone unavailable: {e}")
        return None

    try:
        text = recognizer.recognize_google(audio)  # type: ignore[attr-defined]
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"[EARS ERROR]: Speech recognition service unavailable: {e}")
        return None


if __name__ == "__main__":
    listen()

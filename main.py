import src.ears as ears
import src.brain as brain
import src.voice as voice
import time
import re


def print_banner():
    print("="*60)
    print("   JARVIS: ADVANCED CYBERSECURITY ASSISTANT (V2.5)   ")
    print("   Status: ACTIVE | OSINT & Network Recon Mode       ")
    print("="*60)


def _safe_speak(text: str) -> None:
    try:
        voice.speak(text)
    except Exception as e:
        print(f"[TTS WARNING]: {e}")


def run_jarvis():
    print_banner()
    _safe_speak("All systems nominal. JARVIS is online and monitoring for threats.")

    while True:
        time.sleep(0.3)  # iteration rate guard

        try:
            user_input = ears.listen()

            if user_input is None:
                continue

            if any(word in user_input.lower() for word in ["exit", "stop", "shutdown"]):
                _safe_speak("Shutting down security protocols. Goodbye.")
                break

            print(f"\n[USER]: {user_input}")

            if "scan" in user_input.lower():
                print("[JARVIS]: Initializing deep scan. This may take a moment...")
            else:
                print("[JARVIS]: Analyzing command...")

            response = brain.ask_jarvis(user_input)

            print(f"\n[JARVIS]: {response}\n")

            # Strip markdown/formatting so pyttsx3 doesn't read symbols aloud
            clean_speech = re.sub(r'[`*#_]', '', response)
            clean_speech = re.sub(r'(?m)^[-*]\s+', '', clean_speech)
            clean_speech = re.sub(r'(?m)^\d+\.\s+', '', clean_speech)
            clean_speech = re.sub(r'(?m)^>\s+', '', clean_speech)
            _safe_speak(clean_speech)

        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"\n[ERROR]: {e}")
            _safe_speak("Sir, I encountered an error. Standing by for your next command.")


if __name__ == "__main__":
    try:
        run_jarvis()
    except KeyboardInterrupt:
        print("\n\n[!] Emergency Deactivation Triggered. Systems Offline.")

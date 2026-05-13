import src.ears as ears
import src.brain as brain
import src.voice as voice
import time
import os
import re

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*60)
    print("   JARVIS: ADVANCED CYBERSECURITY ASSISTANT (V2.5)   ")
    print("   Status: ACTIVE | OSINT & Network Recon Mode       ")
    print("="*60)

def run_jarvis():
    print_banner()
    voice.speak("All systems nominal. JARVIS is online and monitoring for threats.")
    
    try:
        while True:
            # 1. Listen for a command
            user_input = ears.listen()
            
            if user_input:
                # Standard Exit Commands
                if any(word in user_input.lower() for word in ["exit", "stop", "shutdown"]):
                    voice.speak("Shutting down security protocols. Goodbye.")
                    break
                
                print(f"\n[USER]: {user_input}")
                
                # Visual feedback for long scans
                if "scan" in user_input.lower():
                    print("[JARVIS]: Initializing deep scan. This may take a moment...")
                else:
                    print("[JARVIS]: Analyzing command...")
                
                # 2. Process with the Brain (Now with Regex & Targeting)
                response = brain.ask_jarvis(user_input)
                
                # 3. Output the result to Terminal
                print(f"\n[JARVIS]: {response}\n")
                
                # 4. Clean up response for Voice
                # Removes Markdown stars and extra symbols for natural speech
                clean_speech = re.sub(r'[*#_]', '', response) 
                voice.speak(clean_speech)
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\n[!] Emergency Deactivation Triggered. Systems Offline.")
    except Exception as e:
        print(f"\n[ERROR]: Critical system failure: {e}")
        voice.speak("Sir, a system error has occurred in the core processing loop.")

if __name__ == "__main__":
    run_jarvis()
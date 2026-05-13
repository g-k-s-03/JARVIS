from google import genai
from google.genai import types
import os
import re
from dotenv import load_dotenv

# Smart Import to handle both root and internal execution
try:
    from src import tools
except ImportError:
    import tools

# 1. Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or "AIzaSyBIzwRwqs2I_4aRHF6U9EnaWRwsBdA-kGE"

# 2. Initialize the 2026 Client
client = genai.Client(api_key=api_key)

def ask_jarvis(prompt):
    """
    Analyzes the user prompt. 
    1. Uses Regex to find IP addresses or Subnets.
    2. Runs Nmap via tools.py if a scan is requested.
    3. Provides cybersecurity intelligence via Gemini for everything else.
    """
    prompt_lower = prompt.lower()
    
    try:
        # --- TOOL TRIGGER LOGIC ---
        if "scan" in prompt_lower:
            print("[!] JARVIS: Detecting target parameters...")
            
            # Regex to identify IPv4 addresses (e.g. 192.168.1.1) 
            # and CIDR notation (e.g. 192.168.1.0/24)
            ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'
            found_targets = re.findall(ip_pattern, prompt_lower)
            
            # Logic for choosing the target
            if found_targets:
                target = found_targets[0]
                print(f"[!] JARVIS: Specific target identified: {target}")
            elif "network" in prompt_lower or "whole" in prompt_lower:
                # Defaulting to a common home network range - update if yours is different
                target = "192.168.1.0/24" 
                print(f"[!] JARVIS: Scaling scan to full network range: {target}")
            else:
                target = "127.0.0.1"
                print(f"[!] JARVIS: No external target found. Defaulting to localhost.")

            # Run the actual scanner
            scan_data = tools.scan_network(target)
            
            # Send results to Gemini to "read" them to you intelligently
            analysis_prompt = (
                f"I performed a security scan on {target}. "
                f"Results found: {scan_data}. "
                "Summarize these findings for a SOC Level 1 analyst. "
                "Highlight active hosts and suspicious open ports."
            )
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction="You are JARVIS. Summarize Nmap results professionally. Be concise but mention all open ports found."
                ),
                contents=analysis_prompt
            )
            return f"[Scan Results for {target}]\n{response.text}"

        # --- STANDARD INTELLIGENCE LOGIC ---
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction="You are JARVIS, a cybersecurity expert. Provide technical, concise intel."
                ),
                contents=prompt
            )
            return response.text

    except Exception as e:
        return f"Brain Error: {str(e)}"

if __name__ == "__main__":
    print("--- JARVIS 2026 ADVANCED TARGETING DEBUG ---")
    
    # Test 1: Intelligence
    print("\n[TEST] Query: 'What is a zero-day exploit?'")
    print("JARVIS:", ask_jarvis("What is a zero-day exploit?"))
    
    print("-" * 40)
    
    # Test 2: Specific IP Target
    print("\n[TEST] Query: 'JARVIS, scan 192.168.1.1'")
    # Note: This will attempt a real scan if Nmap is ready!
    print("JARVIS:", ask_jarvis("JARVIS, scan 192.168.1.1"))
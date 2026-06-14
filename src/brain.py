from google import genai
from google.genai import types
import os
import re
from dotenv import load_dotenv

try:
    from src import tools
    from src import intel
except ImportError:
    import tools  # type: ignore[no-redef]
    import intel  # type: ignore[no-redef]

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY is not set. Add it to your .env file.")

client = genai.Client(api_key=api_key)

_SOC_SYSTEM_PROMPT = (
    "You are JARVIS, a cybersecurity SOC Level 1 assistant. "
    "You ONLY respond to cybersecurity, network security, OSINT, and threat intelligence topics. "
    "If a request falls outside this domain, politely decline and redirect to security topics. "
    "Be concise, technical, and professional."
)

_CONTROL_CHAR_RE = re.compile(r'[\x00-\x1f\x7f]')


def _sanitise_input(text: str) -> str:
    text = text[:500]
    return _CONTROL_CHAR_RE.sub('', text)


def ask_jarvis(prompt: str) -> str:
    prompt = _sanitise_input(prompt)
    prompt_lower = prompt.lower()

    try:
        if "scan" in prompt_lower:
            print("[!] JARVIS: Detecting target parameters...")

            ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'
            found_targets = re.findall(ip_pattern, prompt_lower)

            if found_targets:
                target = found_targets[0]
                print(f"[!] JARVIS: Specific target identified: {target}")
            elif "network" in prompt_lower or "whole" in prompt_lower:
                target = "192.168.1.0/24"
                print(f"[!] JARVIS: Scaling scan to full network range: {target}")
            else:
                target = "127.0.0.1"
                print("[!] JARVIS: No external target found. Defaulting to localhost.")

            scan_data = tools.scan_network(target)

            analysis_prompt = (
                f"I performed a security scan on {target}. "
                f"Results found: {scan_data}. "
                "Summarize these findings for a SOC Level 1 analyst. "
                "Highlight active hosts and suspicious open ports."
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are JARVIS. Summarize Nmap results professionally. "
                        "Be concise but mention all open ports found."
                    )
                ),
                contents=analysis_prompt
            )
            return f"[Scan Results for {target}]\n{response.text}"

        elif any(word in prompt_lower for word in ["locate", "geolocate", "where is"]):
            ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
            found_ips = re.findall(ip_pattern, prompt_lower)
            if found_ips:
                return intel.geolocate_ip(found_ips[0])
            return "No IP address found in your request. Please specify an IP to locate."

        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=_SOC_SYSTEM_PROMPT
                ),
                contents=prompt
            )
            return response.text

    except Exception as e:
        return f"Brain Error: {str(e)}"


if __name__ == "__main__":
    print("--- JARVIS BRAIN DEBUG ---")
    print("\n[TEST] Query: 'What is a zero-day exploit?'")
    print("JARVIS:", ask_jarvis("What is a zero-day exploit?"))

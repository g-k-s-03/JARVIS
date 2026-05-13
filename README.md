# JARVIS: Advanced Voice-Activated SOC Assistant (V2.5)

An AI-powered cybersecurity orchestrator designed for rapid network reconnaissance and OSINT intelligence. This project is optimized for **SOC Level 1 Analysts** and law enforcement investigations.

## 🚀 Key Features
- **Voice-Command Interface:** Hands-free operation for field investigators.
- **Advanced Network Recon:** Uses **ARP Discovery (-PR)** to eliminate false positives in local subnets.
- **OSINT Intelligence:** Real-time Geolocation and ISP lookup for external IP addresses.
- **AI-Driven Analysis:** Powered by **Gemini 2.5-Flash** to translate raw Nmap data into actionable security reports.

## 🛠️ Usage & Commands
Once the system is active, JARVIS will listen for specific triggers. Use the following voice commands:

### 1. Local Network Discovery
- **Command:** *"Scan the whole network"* or *"Scan network 192.168.1.0/24"*
- **Result:** Performs an ARP-based discovery scan to find all active physical devices on your subnet.

### 2. Targeted Vulnerability Scan
- **Command:** *"Run a scan on [IP Address]"* (e.g., *"Run a scan on 127.0.0.1"*)
- **Result:** Executes a fast port scan and service version detection.

### 3. OSINT & Geolocation
- **Command:** *"Locate IP [IP Address]"* (e.g., *"Locate IP 8.8.8.8"*)
- **Result:** Fetches the city, country, ISP, and organization associated with the target IP.

## 🏗️ System Architecture

1. **Sense:** Voice capture via `ears.py`.
2. **Think:** Intent analysis and AI contextualization in `brain.py`.
3. **Act:** Nmap execution (`tools.py`) and API calls (`intel.py`).
4. **Feedback:** Audio reporting via `voice.py`.

## 📦 Installation
1. Clone the repo: `git clone https://github.com/tejas9783/JARVIS.git`
2. Install requirements: `pip install -r requirements.txt`
3. Add your `GEMINI_API_KEY` to the `.env` file.
4. Run: `python main.py`

## 🛡️ Security Disclaimer
This tool is for **authorized security research and law enforcement use only**.
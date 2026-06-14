import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()
_IPGEO_API_KEY = os.getenv("IPGEO_API_KEY")

_IPV4_RE = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}$')


def geolocate_ip(ip: str) -> str:
    if not _IPV4_RE.match(ip):
        return f"Geolocation aborted: '{ip}' is not a valid IPv4 address."

    try:
        url = f"https://ipapi.co/{ip}/json/"
        params = {}
        if _IPGEO_API_KEY:
            params["key"] = _IPGEO_API_KEY

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            return f"Geolocation Error: {data.get('reason', 'Unknown error from API')}"

        return (
            f"IP: {data.get('ip', ip)} | "
            f"Country: {data.get('country_name', 'Unknown')} | "
            f"Region: {data.get('region', 'Unknown')} | "
            f"City: {data.get('city', 'Unknown')} | "
            f"ISP: {data.get('org', 'Unknown')}"
        )

    except requests.exceptions.HTTPError as e:
        return f"Geolocation Error: HTTP {e.response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Geolocation Error: Could not connect to the geolocation service."
    except requests.exceptions.Timeout:
        return "Geolocation Error: Request timed out after 10 seconds."
    except Exception as e:
        return f"Geolocation Error: {str(e)}"


if __name__ == "__main__":
    print(geolocate_ip("8.8.8.8"))

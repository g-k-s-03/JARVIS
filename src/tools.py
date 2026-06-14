import nmap
import re

# Accepts IPv4, IPv4/CIDR, or simple hostnames (no shell metacharacters)
_TARGET_RE = re.compile(
    r'^(?:'
    r'(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?'                         # IPv4 or CIDR
    r'|'
    r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*'       # hostname labels
    r'[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
    r')$'
)


def scan_network(target: str = "127.0.0.1") -> str:
    """
    Performs an Nmap scan on a single target or a range (CIDR).
    Validates the target before passing it to nmap to prevent injection.
    """
    if not _TARGET_RE.match(target):
        return f"Scan aborted: '{target}' is not a valid IPv4, CIDR, or hostname."

    try:
        nm = nmap.PortScanner()

        if "/" in target:
            print(f"[!] JARVIS: Performing Host Discovery on network {target}...")
            nm.scan(hosts=target, arguments='-sn -T4', timeout=60)
        else:
            print(f"[!] JARVIS: Running Fast Port Scan on {target}...")
            nm.scan(hosts=target, arguments='-F -T4', timeout=60)

        scan_results = ""

        for host in nm.all_hosts():
            state = nm[host].state()
            hostname = nm[host].hostname()
            scan_results += f"\nHost: {host} ({hostname or 'Unknown Name'})\n"
            scan_results += f"Status: {state}\n"

            if "/" not in target:
                for proto in nm[host].all_protocols():
                    scan_results += f"Protocol: {proto.upper()}\n"
                    for port in sorted(nm[host][proto].keys()):
                        port_state = nm[host][proto][port]['state']
                        service = nm[host][proto][port]['name']
                        scan_results += f"  - Port {port} ({service}): {port_state}\n"

        return scan_results or "Scan completed: No active hosts or open ports detected."

    except nmap.PortScannerError as e:
        return f"Nmap Error: {str(e)}"
    except Exception as e:
        return f"Nmap Scanner Error: {str(e)}"


if __name__ == "__main__":
    print(scan_network("127.0.0.1"))

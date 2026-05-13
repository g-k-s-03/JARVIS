import nmap

def scan_network(target="127.0.0.1"):
    """
    Performs an Nmap scan on a single target or a range (CIDR).
    Differentiates between 'Ping Scans' for networks and 'Port Scans' for specific IPs.
    """
    try:
        nm = nmap.PortScanner()
        
        # Logic: If it's a subnet (/24), we do a Ping Scan (-sn) to find live hosts quickly.
        # If it's a specific IP, we do a Fast Port Scan (-F).
        if "/24" in target:
            print(f"[!] JARVIS: Performing Host Discovery on network {target}...")
            # -sn: Ping scan (No port scan), -T4: Faster execution
            nm.scan(hosts=target, arguments='-sn -T4')
        else:
            print(f"[!] JARVIS: Running Fast Port Scan on {target}...")
            # -F: Fast mode (scans fewer ports), -T4: Aggressive timing
            nm.scan(hosts=target, arguments='-F -T4')

        scan_results = ""
        
        # Iterate through all discovered hosts
        for host in nm.all_hosts():
            state = nm[host].state()
            hostname = nm[host].hostname()
            
            scan_results += f"\nHost: {host} ({hostname if hostname else 'Unknown Name'})\n"
            scan_results += f"Status: {state}\n"

            # Only attempt to list ports if we did a port scan (not a subnet ping scan)
            if "/24" not in target:
                for proto in nm[host].all_protocols():
                    scan_results += f"Protocol: {proto.upper()}\n"
                    ports = sorted(nm[host][proto].keys())
                    for port in ports:
                        port_state = nm[host][proto][port]['state']
                        service = nm[host][proto][port]['name']
                        scan_results += f"  - Port {port} ({service}): {port_state}\n"
        
        if not scan_results:
            return "Scan completed: No active hosts or open ports detected."
            
        return scan_results

    except Exception as e:
        return f"Nmap Scanner Error: {str(e)}"

if __name__ == "__main__":
    # Internal test for localhost
    print(scan_network("127.0.0.1"))
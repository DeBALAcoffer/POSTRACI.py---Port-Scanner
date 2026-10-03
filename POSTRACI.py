"""
POSTRACI - Multi-threaded TCP Port Scanner
by DeBALA
"""

import socket
import argparse
import sys
import time
import threading
from typing import List, Tuple

# ANSI Color Codes
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[1;31m"
COLOR_GREEN = "\033[1;32m"
COLOR_YELLOW = "\033[1;33m"
COLOR_CYAN = "\033[1;36m"

BANNER = r"""
 _______    ______    ______   ________  _______    ______    ______   ______ 
/       \  /      \  /      \ /        |/       \  /      \  /      \ /      |
$$$$$$$  |/$$$$$$  |/$$$$$$  |$$$$$$$$/ $$$$$$$  |/$$$$$$  |/$$$$$$  |$$$$$$/ 
$$ |__$$ |$$ |  $$ |$$ \__$$/    $$ |   $$ |__$$ |$$ |__$$ |$$ |  $$/   $$ |  
$$    $$/ $$ |  $$ |$$      \    $$ |   $$    $$< $$    $$ |$$ |        $$ |  
$$$$$$$/  $$ |  $$ | $$$$$$  |   $$ |   $$$$$$$  |$$$$$$$$ |$$ |   __   $$ |  
$$ |      $$ \__$$ |/  \__$$ |   $$ |   $$ |  $$ |$$ |  $$ |$$ \__/  | _$$ |_ 
$$ |      $$    $$/ $$    $$/    $$ |   $$ |  $$ |$$ |  $$ |$$    $$/ / $$   |
$$/        $$$$$$/   $$$$$$/     $$/    $$/   $$/ $$/   $$/  $$$$$$/  $$$$$$/ 
"""

# Thread-safe lock for printing
print_lock = threading.Lock()

def parse_ports(port_input: str) -> List[int]:
    """Parse port input like '1-100' or '22,80,443' into a list of ports."""
    ports = []
    for segment in port_input.split(','):
        if '-' in segment:
            start, end = map(int, segment.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(segment))
    return ports

def scan_port(host: str, port: int, timeout: int, open_ports: list):
    """Scan a single port and add to open_ports list if open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            with print_lock:
                open_ports.append(port)
                print(f"{COLOR_GREEN}[+] Port {port} is OPEN{COLOR_RESET}")
    except Exception:
        pass

def main():
    print(f"{COLOR_CYAN}{BANNER}{COLOR_RESET}")

    parser = argparse.ArgumentParser(
        description=f"{COLOR_CYAN}POSTRACI Configuration{COLOR_RESET}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""{COLOR_YELLOW}Usage Examples:{COLOR_RESET}

  1. Quick Localhost Scan:
     python POSTRACI.py -H 127.0.0.1 -P 1-100

  2. Service Hunter (specific ports):
     python POSTRACI.py -H scanme.nmap.org -P 22,80,443,3306

  3. Standard Sweep (well-known ports):
     python POSTRACI.py -H scanme.nmap.org -P 1-1024

  4. Speed Demon (high concurrency):
     python POSTRACI.py -H scanme.nmap.org -P 1-1024 -W 300

  5. Patient Scanner (long timeout):
     python POSTRACI.py -H scanme.nmap.org -P 1-100 -D 5

  6. Localhost Deep Dive:
     python POSTRACI.py -H 127.0.0.1 -P 1-1000 -W 200

  7. Full Port Scan:
     python POSTRACI.py -H 127.0.0.1 -P 1-65535 -W 500

  8. Firewall Timeout Test:
     python POSTRACI.py -H 192.0.2.1 -P 1-50 -D 3

  9. Save Results to File:
     python POSTRACI.py -H scanme.nmap.org -P 1-100 > report.txt

{COLOR_RED}Legal Notice:{COLOR_RESET}
  Only scan systems you own or have explicit permission to test.
  scanme.nmap.org is a legal testing server provided by Nmap.

{COLOR_CYAN}[i] POSTRACI is developed and maintained by DeBALA.{COLOR_RESET}
""")

    parser.add_argument('-H', '--host', default='127.0.0.1',
                        help='Target hostname or IP (default: 127.0.0.1)')
    parser.add_argument('-P', '--ports', default='1-1024',
                        help='Ports to scan (e.g. 1-1024 or 22,80,443)')
    parser.add_argument('-W', '--workers', type=int, default=100,
                        help='Number of concurrent workers (default: 100)')
    parser.add_argument('-D', '--delay', type=int, default=2,
                        help='Connection timeout in seconds (default: 2)')

    args = parser.parse_args()

    # Parse ports
    ports_to_scan = parse_ports(args.ports)

    # Display scan info
    print(f"{COLOR_GREEN}[*] Starting POSTRACI scan...{COLOR_RESET}")
    print(f"    Target:    {COLOR_YELLOW}{args.host}{COLOR_RESET}")
    print(f"    Ports:     {COLOR_YELLOW}{args.ports} ({len(ports_to_scan)} ports){COLOR_RESET}")
    print(f"    Workers:   {COLOR_YELLOW}{args.workers}{COLOR_RESET}")
    print(f"    Timeout:   {COLOR_YELLOW}{args.delay}s{COLOR_RESET}\n")

    # Start timer
    start_time = time.time()

    # Multi-threaded scanning using threading module
    open_ports = []
    threads = []
    semaphore = threading.Semaphore(args.workers)

    def worker(port):
        semaphore.acquire()
        try:
            scan_port(args.host, port, args.delay, open_ports)
        finally:
            semaphore.release()

    for port in ports_to_scan:
        t = threading.Thread(target=worker, args=(port,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # End timer
    end_time = time.time()
    duration = end_time - start_time

   
    print(f"\n{COLOR_GREEN}[+] Scan finished in {duration:.2f} seconds.{COLOR_RESET}")
    print(f"{COLOR_GREEN}[+] Found {len(open_ports)} open port(s).{COLOR_RESET}")
    print(f"{COLOR_CYAN}Built by DeBALA.{COLOR_RESET}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# PyScan Pro - TCP Port Scanner

import socket
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== CONFIG =====
MAX_THREADS = 100
TIMEOUT = 0.5

# ===== COLOR =====
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

# ===== BANNER =====
def banner():
    print(f"""{GREEN}
╔══════════════════════════════╗
║        Author: DUCVIET1622   ║
║   Multi-thread Port Scanner  ║
╚══════════════════════════════╝
{RESET}""")

# ===== PROGRESS BAR =====
def progress_bar(current, total, length=30):
    percent = current / total
    filled = int(length * percent)
    bar = '█' * filled + '-' * (length - filled)
    sys.stdout.write(f"\r{CYAN}[{bar}] {current}/{total} ({percent*100:.0f}%){RESET}")
    sys.stdout.flush()

# ===== SCAN 1 PORT =====
def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            return (port, service)
    except:
        pass
    return None

# ===== MAIN =====
def main():
    banner()

    try:
        target_input = input(f"{YELLOW}[?] IP/Host: {RESET}").strip()
        ip = socket.gethostbyname(target_input)
    except:
        print(f"{RED}[-] Host không hợp lệ!{RESET}")
        input("Enter để thoát...")
        return

    port_str = input(f"{YELLOW}[?] Port (vd 1-1024): {RESET}").strip()

    try:
        if '-' in port_str:
            start_port, end_port = map(int, port_str.split('-'))
        else:
            start_port = end_port = int(port_str)

        if start_port < 1 or end_port > 65535:
            raise ValueError
    except:
        print(f"{RED}[-] Dải port không hợp lệ!{RESET}")
        input("Enter để thoát...")
        return

    total = end_port - start_port + 1

    print(f"\n{YELLOW}[*] Target: {ip}{RESET}")
    print(f"{YELLOW}[*] Scan: {start_port}-{end_port}{RESET}")
    print(f"{YELLOW}[*] Đang quét...\n{RESET}")

    start_time = datetime.now()
    open_ports = []
    done = 0

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(scan_port, ip, p) for p in range(start_port, end_port + 1)]

        for future in as_completed(futures):
            result = future.result()
            done += 1

            if result:
                port, service = result
                print(f"\n{GREEN}[+] PORT {port} OPEN → {service}{RESET}")
                open_ports.append(result)

            progress_bar(done, total)

    print()  # xuống dòng

    elapsed = (datetime.now() - start_time).total_seconds()

    print("\n" + "="*40)
    print(f"{GREEN}[✓] DONE{RESET}")
    print(f"{YELLOW}Time: {elapsed:.2f}s{RESET}")
    print(f"{GREEN}Open ports: {len(open_ports)}{RESET}")

    if open_ports:
        print(f"\n{GREEN}PORT     SERVICE{RESET}")
        print(f"{GREEN}{'-'*25}{RESET}")
        for port, service in open_ports:
            print(f"{port:<8} {service}")
    else:
        print(f"{RED}Không có port mở{RESET}")

    input("\nNhấn Enter để thoát...")

# ===== RUN =====
if __name__ == "__main__":
    main()
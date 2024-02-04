from scapy.all import *

conf.checkIPaddr = False

DHCP_DICSCOVER = Ether(dst='ff:ff:ff:ff:ff:ff', src=RandMAC(), type=0x0800) \
        / IP(src='0.0.0.0', dst='255.255.255.255') \
        / UDP(dport=67, sport=68) \
        / BOOTP(op=1, chaddr=RandMAC()) \
        / DHCP(options=[('message-type', 'discover'), ('end')])

sendp(DHCP_DICSCOVER, iface='enp4s0f2', loop=1, verbose=1)

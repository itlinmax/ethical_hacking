from scapy.all import ARP, Ether, srp
target_ip = "10.1.1.10/24"
arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether / arp
# srp() function sends and receives packets at layer 2
result = srp(packet, timeout=10, verbose=0)[0]
clients = []
for sent, received in result:
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})
print("Available devices in the network:")
print("IP" + " " * 18 + "MAC")
for client in clients:
    print(f"{client['ip']:16} {client['mac']}")

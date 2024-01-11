import ipinfo
import sys

try:
    ip_address = sys.argv[1]
except IndexError:
    ip_address = None

access_token = ''

handler = ipinfo.getHandler(access_token)
details = handler.getDetails(ip_address)

for key, value in details.all.items():
    print(f"{key}: {value}")

import whois
import json
from domain_validator import is_registered

domain_name = "google.com"
whois_info = whois.whois(domain_name)
print("WHOIS server:", whois_info.whois_server)
print("Domain creation date:", whois_info.creation_date)
print("Expiration date:", whois_info.expiration_date)
print(whois_info)

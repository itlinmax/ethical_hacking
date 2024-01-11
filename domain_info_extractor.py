import requests
import whois
import dns.resolver
import argparse

def is_registered(domain_name):
    """A function that returns a boolean indicating
       whether a `domain_name` is registered"""

    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)

def get_discovered_subdomains(domain, subdomain_list, timeout=2):
    discovered_subdomains = []
    for subdomain in subdomain_list:
        url = f"http://{subdomain.strip()}.{domain}"
        try:
            requests.get(url, timeout=timeout)
        except (requests.ConnectionError, requests.ReadTimeout):
            pass
        else:
            print("[+] Discovered subdomain:", url)
            discovered_subdomains.append(url)
    return discovered_subdomains

def resolve_dns_records(target_domain):
    record_types = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]
    resolver = dns.resolver.Resolver()
    for record_type in record_types:
        try:
            answers = resolver.resolve(target_domain, record_type)
        except dns.resolver.NoAnswer:
            continue
        print(f"DNS records for {target_domain} ({record_type}):" )
        for rdata in answers:
            print(f"\t{str(rdata)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Domain name information extractor, uses WHOIS db and scans for subdomains")
    parser.add_argument("domain", help = "The domain name without http(s)")
    parser.add_argument("-t" , "--timeout", type = int, default = 2, help = "The timeout in seconds for prompting the connection, default is 2")
    parser.add_argument("-s" , "--subdomains", default = "subdomains.txt" ,help = "The file path that contains the list of subdomains to scan, default is subdomains.txt")
    parser.add_argument( "-o" , "--output", help = "The output file path resulting the discovered subdomains, default is {domain}-subdomains.txt")
    args = parser.parse_args()

    if is_registered(args.domain):
        whois_info = whois.whois(args.domain)
        print("Domain registrar:", whois_info.registrar)
        print("WHOIS server:", whois_info.whois_server)
        print("Domain creation date:", whois_info.creation_date)
        print("Expiration date:", whois_info.expiration_date)
        print(whois_info)
        print("=" * 50, "DNS records", "=" * 50)
        resolve_dns_records(args.domain)
        print("=" * 50, "Scanning subdomains", "=" * 50)

        with open(args.subdomains, "r", encoding="utf-8") as file:
            subdomains = file.readlines()
        discovered_subdomains = get_discovered_subdomains(args.domain, subdomains, timeout=args.timeout)
        prefix_file = args.output if args.output else args.domain
        discovered_subdomains_file = f"{prefix_file}-subdomains.txt"
        with open(discovered_subdomains_file, "w", encoding="utf-8") as f:
            for subdomain in discovered_subdomains:
                print(subdomain, file=f)

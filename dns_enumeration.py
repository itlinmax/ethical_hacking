import dns.resolver
target_domain = "thepythoncode.com"
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

import os
from momonfunctions import extract_parse_clients
from momonfunctions import extract_bgp_network


file_path = "clientips.txt"
os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)
print(f"{unique_ips}\n")

bgp_networks = extract_bgp_network(unique_ips)

import os
from momonfunctions import extract_parse_clients
from momonfunctions import extract_bgp_network
from momonfunctions import extract_bgp_netname


file_path = "clientips.txt"
os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)
bgp_networks = extract_bgp_network(unique_ips)
extract_bgp_netname(bgp_networks)

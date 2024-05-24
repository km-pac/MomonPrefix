from momonfunctions import *


file_path = "clientips.txt"
os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)
bgp_networks = extract_bgp_network(unique_ips)
print(bgp_networks)
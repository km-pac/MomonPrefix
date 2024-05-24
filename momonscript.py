import os
from testpingmomon import extract_parse_clients
from testpingmomon import extract_bgp_network

file_path = "clientips.txt"
os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)

extract_bgp_network(unique_ips)
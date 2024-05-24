from momonfunctions import *


file_path = "clientips.txt"
os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)
extract_bgp_network(unique_ips)
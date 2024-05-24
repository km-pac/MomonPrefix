import os
from momonfunctions import extract_parse_clients
from momonfunctions import extract_bgp_network
from momonfunctions import extract_bgp_netname

target_url = "https://bgp.he.net/ip/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build\\/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
}
file_path = "clientips.txt"
os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)

bgp_networks = extract_bgp_network(target_url, headers, unique_ips)
extract_bgp_netname(target_url, headers, bgp_networks)

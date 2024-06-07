import os
from momonfunctions import extract_parse_clients
from momonfunctions import extract_bgp_network
from momonfunctions import extract_netname
from momonfunctions import extract_final_hop

target_url = "https://bgp.he.net/ip/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build\\/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
}
file_path = "clientips.txt"
os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)

bgp_networks = extract_bgp_network(target_url, headers, unique_ips)
bgp_netname = extract_netname("BGP", target_url, headers, bgp_networks)

alive_addresses, last_hops = extract_final_hop(bgp_networks)
last_hops_netname = extract_netname("LAST LOP", target_url, headers, last_hops)

for count, bgp_prefix in enumerate(bgp_networks):
    print(count, bgp_prefix, bgp_netname[count], alive_addresses[count], last_hops[count], last_hops_netname[count])
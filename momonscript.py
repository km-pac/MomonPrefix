import os, time
from colorama import Fore, Style, init
from momonfunctions import extract_parse_clients
from momonfunctions import extract_bgp_network
from momonfunctions import extract_netname
from momonfunctions import extract_final_hop
from momonfunctions import loading_style
from momonfunctions import title_spacing, index_spacing, ip_spacing

init(autoreset = True)

target_url = "https://bgp.he.net/ip/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build\\/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
}
file_path = "clientips.txt"

os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)
bgp_networks = extract_bgp_network(target_url, headers, unique_ips)

os.system("clear")
# bgp_netname = extract_netname("BGP", target_url, headers, bgp_networks)

os.system("clear")
alive_addresses, last_hops = extract_final_hop(bgp_networks)

os.system("clear")
last_hops_netname = extract_netname("LAST LOP", target_url, headers, last_hops)

os.system("clear")
print(f"{loading_style}\n{'>> ':<{title_spacing}}TWMON SUMMARY: TO BE EXPORTED{' ':<{title_spacing}}\n{'IDX':<{index_spacing}} {'BGP IP':<{ip_spacing}} {'PINGABLE IP':<{ip_spacing}} {'LAST HOP':<{ip_spacing}} {'LAST HOP ISP':<{ip_spacing}}")
for count, bgp_prefix in enumerate(bgp_networks):
    print(f"{loading_style}{count+1:<{index_spacing}} {bgp_prefix:<{ip_spacing}} {alive_addresses[count]:<{ip_spacing}} {last_hops[count]:<{ip_spacing}} {last_hops_netname[count]:<{ip_spacing}}")
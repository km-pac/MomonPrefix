import os, concurrent.futures
from colorama import Fore, Style, init
from momonfunctions import extract_parse_clients
from momonfunctions import extract_bgp_network
from momonfunctions import extract_netname
from momonfunctions import extract_final_hop
from momonfunctions import success_style
from momonfunctions import title_spacing, index_spacing, ip_spacing
from threadingtest import extract_bgp_networkT

init(autoreset = True)

target_url = "https://bgp.he.net/ip/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
file_path = "clientips.txt"

parsed_bgp_networks = list()

os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)
# bgp_networks = extract_bgp_network(target_url, headers, unique_ips)
with concurrent.futures.ThreadPoolExecutor() as executor:
    bgp_networks = list(executor.map(extract_bgp_networkT, unique_ips))

for ip in bgp_networks:
    parsed_bgp_networks.append(ip.replace("[","").replac("]","").replace("\"\"",""))

os.system("clear")
# bgp_netname = extract_netname("BGP", target_url, headers, bgp_networks)

os.system("clear")
alive_addresses, last_hops = extract_final_hop(parsed_bgp_networks)

os.system("clear")
last_hops_netname = extract_netname("LAST LOP", target_url, headers, last_hops)

os.system("clear")
print(f"{success_style}\n{'>> ':<{title_spacing}}TWMON SUMMARY: TO BE EXPORTED{' ':<{title_spacing}}\n{'IDX':<{index_spacing}} {'BGP IP':<{ip_spacing}} {'PINGABLE IP':<{ip_spacing}} {'LAST HOP':<{ip_spacing}} {'LAST HOP ISP':<{ip_spacing}}")
for count, bgp_prefix in enumerate(bgp_networks):
    print(f"{success_style}{count+1:<{index_spacing}} {bgp_prefix:<{ip_spacing}} {alive_addresses[count]:<{ip_spacing}} {last_hops[count]:<{ip_spacing}} {last_hops_netname[count]:<{ip_spacing}}")

import requests, os, concurrent.futures
from colorama import Fore, Style, init
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from IPy import IP

init(autoreset = True)

title_spacing = 5
index_spacing = 5
ip_spacing = 22
end_spacing = 50
timeout_count = 2
title_style = Fore.CYAN + Style.BRIGHT
success_style = Fore.GREEN + Style.BRIGHT
sub_style = Fore.MAGENTA + Style.BRIGHT
error_style = Fore.RED + Style.BRIGHT
enableDebugMessage = False

target_url = "https://bgp.he.net/ip/"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def extract_parse_clients(file_path):
	with open(file_path, 'r') as file: 
		lines = file.readlines() 
		extracted_ips = [line.strip() for line in lines]
		unique_ips = sorted(list(set(extracted_ips)))
		print(f"EXTRACTED CLIENT IPs: {len(extracted_ips)}\nUNIQUE CLIENT IPs: {len(unique_ips)}\n")
	return extracted_ips, unique_ips

def extract_bgp_networkT(unique_ip):
    bgp_prefixes = list()
    print(f"Checking for BGP Prefix of {unique_ip}", end="\r", flush=True)
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(target_url + unique_ip,   
    headers=headers)
    data = response.text
    try:
        parsed_bgp_prefix = data.strip().split("/net/")[1].split("\">")[0]
        # parsed_bgp_prefix = data.split("<span><a href=")[1].split("/prefix/")[1].split("\">")[0] 
    except:
        parsed_bgp_prefix = "N/A"
    print(f"{success_style}{unique_ip:<{ip_spacing}}    {parsed_bgp_prefix:<{end_spacing}}")
    return bgp_prefixes

def extract_netname(ip_address):
    bgp_netnames = list()
    print(f"Checking for ISP of {ip_address}", end="\r", flush=True)
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(target_url + ip_address, headers=headers)
    data = response.text
    try:
        isp_count = data.count("break-word;\">")
        parsed_bgp_netnames = (data.split("break-word;\">")[isp_count].split("</td>")[0])
    except:
        parsed_bgp_netnames = "N/A"
    bgp_netnames.append(parsed_bgp_netnames)
    print(f"{success_style}{'CLIENT IP:':<{index_spacing}} {ip_address:<{ip_spacing}} {'BGP PREFIX:':<{index_spacing}} {parsed_bgp_netnames:<{end_spacing}}")
    return bgp_netnames

# def extract_activeip(bgp_prefix):
#     active_ips = list()
#     command = f"timeout 20s fping -a -g -q {bgp_prefix}"
#     process = os.popen(command)
#     for line in process:
#         if line is not None:
#             isAlive = True
#             parsed_active_ip = line.split(" ")[0].strip()
#             break
#         if not isAlive: 
#             parsed_active_ip = "N/A"
#         active_ips.append(parsed_active_ip)
#     print(f"{success_style}{'BGP PREFIX:':<{index_spacing}} {bgp_prefix:<{ip_spacing}} {'ACTIVE IP:':<{index_spacing}} {parsed_active_ip:<{end_spacing}}")
#     return active_ips

# def extract_activeip(bgp_prefix):
#     active_ips = list()
#     command = f"timeout 30s fping -a -g -q {bgp_prefix}"
#     process = os.popen(command)
    
#     parsed_active_ip = "N/A"
    
#     for line in process:
#         if line is not None or "ICMP" not in line:
#             parsed_active_ip = line.split(" ")[0].strip()
#             break
#         else:
#             parsed_active_ip = "N/A"
#     active_ips.append(parsed_active_ip)
    
#     print(f"{success_style}{'BGP PREFIX:':<{index_spacing}} {bgp_prefix:<{ip_spacing}} {'ACTIVE IP:':<{index_spacing}} {parsed_active_ip:<{end_spacing}}")
    
#     return active_ips





file_path = "clientips.txt"

os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)

proccesses = []
with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
    # bgp_prefixes = executor.map(extract_bgp_networkT, unique_ips)
    bgp_prefixes = list(executor.map(extract_bgp_networkT, unique_ips))
    print('\n'.join(str(x[0]) + ', ' + str(x[1]) for x in bgp_prefixes))


    # proccesses.append(executor.map(extract_bgp_networkT, unique_ips))
    # for ip in concurrent.futures.as_completed(proccesses):
    #         print('Result: ', ip.result())
    #         os.system(f"echo {ip.result()} >> bgp_prefixes.txt")
    
         

    # # Use executor.map directly on bgp_prefixes to apply extract_activeip function in parallel
    # active_addresses = list(executor.map(extract_activeip, unique_ips))
    
    # Print or process each element in active_addresses
    # for addr in active_addresses:
    #     print(addr)
    


    # bgp_netnames = list(executor.map(extract_netname, ip) for ip in bgp_prefixes)

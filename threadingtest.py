import requests, os, time, datetime, concurrent.futures
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

target_url = "https://bgpview.io/ip/"
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

def extract_bgp_network(unique_ip):
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
        parsed_bgp_prefix = data.split("<span><a href=")[1].split("/prefix/")[1].split("\">")[0] 
    except:
        parsed_bgp_prefix = "N/A"
    bgp_prefixes.append(parsed_bgp_prefix)
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

def extract_activeip(bgp_prefix):
    command = f"timeout 20s fping -a -g -q {bgp_prefix}"
    process = os.popen(command)
    for line in process:
        if line is not None:
            isAlive = True
            active_addresses = line.split(" ")[0].strip()
            break
        if not isAlive: 
            active_addresses = "N/A"
    return active_addresses







file_path = "clientips.txt"

os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)


with concurrent.futures.ThreadPoolExecutor() as executor:
    # Fill bgp_prefixes list first
    bgp_prefixes = list(executor.map(extract_bgp_network, unique_ips))
    print(bgp_prefixes)
    
    # Now use bgp_prefixes to extract active addresses one by one
    active_addresses = []
    for prefix in bgp_prefixes:
        active_addresses.extend(executor.map(extract_bgp_network, prefix))
    print(active_addresses)

    # bgp_netnames = list(executor.map(extract_netname, ip) for ip in bgp_prefixes)

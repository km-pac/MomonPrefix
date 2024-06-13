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

def extract_parse_clients(file_path):
	with open(file_path, 'r') as file: 
		lines = file.readlines() 
		extracted_ips = [line.strip() for line in lines]
		unique_ips = sorted(list(set(extracted_ips)))
		print(f"EXTRACTED CLIENT IPs: {len(extracted_ips)}\nUNIQUE CLIENT IPs: {len(unique_ips)}\n")
	return extracted_ips, unique_ips

def extract_bgp_network(unique_ip):
    parsed_bgp_netnames = list()
    target_url = "https://bgpview.io/ip/"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    
    print(f"Checking for BGP Prefix of {unique_ip}", end="\r", flush=True)

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(target_url + unique_ip, headers=headers)
    data = response.text
    
    parsed_bgp_prefix = data.split("<span><a href=")[1].split("/prefix/")[1].split("\">")[0]
    
    isp_count = data.count("break-word;\">")
    parsed_bgp_netnames.append(data.split("break-word;\">")[isp_count].split("</td>")[0])
    print(parsed_bgp_netnames)
    
    print(f"{success_style}{unique_ip:<{ip_spacing}} {parsed_bgp_prefix:<{end_spacing}}")

file_path = "clientips.txt"

os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)

with concurrent.futures.ThreadPoolExecutor() as executor:
	executor.map(extract_bgp_network, unique_ips)
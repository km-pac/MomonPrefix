import requests, os, time
from colorama import Fore, Style, init
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from IPy import IP

init(autoreset = True)

title_spacing = 5
index_spacing = 5
ip_spacing = 22
end_spacing = 50
timeout_count = 5
title_style = Fore.CYAN + Style.BRIGHT
success_style = Fore.GREEN + Style.BRIGHT
sub_style = Fore.MAGENTA + Style.BRIGHT
error_style = Fore.RED + Style.BRIGHT
enableDebugMessage = True

class ExtractedIP:
	def	__init__(self, client_ip, bgp_network, isp_netname):
		self.client_ip = client_ip
		self.bgp_network = bgp_network
		self.isp_netname = isp_netname

def extract_parse_clients(file_path):
	with open(file_path, 'r') as file: 
		lines = file.readlines() 
		extracted_ips = [line.strip() for line in lines]
		unique_ips = sorted(list(set(extracted_ips)))
		print(f"{sub_style}EXTRACTED CLIENT IPs: {len(extracted_ips)}\nUNIQUE CLIENT IPs: {len(unique_ips)}\n")
	return extracted_ips, unique_ips

def extract_bgp_network(target_url, headers, unique_ips):
	parsed_bgp_networks = list()
	bgp_networks = list()
	print(f"{title_style}{'>> ':<{title_spacing}}EXTRACTING BGP NETWORK{' ':<{title_spacing}}\n{'IDX':<{index_spacing}} {'CLIENT IP':<{ip_spacing}} {'NETWORK/PREFIX LENGTH':<{ip_spacing}}")

	for count, ip in enumerate(unique_ips):
		print(f"{count+1:<{index_spacing}} {ip:<{ip_spacing}} {sub_style}Checking for BGP Prefix", end="\r", flush=True)
		
		session = requests.Session()
		retry = Retry(connect=3, backoff_factor=0.5)
		adapter = HTTPAdapter(max_retries=retry)
		session.mount('http://', adapter)
		session.mount('https://', adapter)

		response = session.get(target_url + ip, headers=headers)
		data = response.text
		
		try: 
			client_ip = [line for line in data.split('\n') if "/net/" in line][0]
			parsed_network_ip = client_ip.strip().split("/net/")[1].split("\">")[0]
			parsed_bgp_networks.append(parsed_network_ip)
			print(f"{success_style}{count+1:<{index_spacing}} {ip:<{ip_spacing}} {parsed_network_ip:<{end_spacing}}")
		except: continue
		# if count == 3: break
	bgp_networks = sorted(set(parsed_bgp_networks))
	print(f"{sub_style}\nEXTRACTED BGP NET: {len(parsed_bgp_networks)}\nUNIQUE BGP NET: {len(bgp_networks)}")
	time.sleep(timeout_count)
	return bgp_networks

def extract_netname(category ,target_url, headers, networks):
	parsed_netname = list()
	network_netname = list()
	print(f"{title_style}\n{'>> ':<{title_spacing}}EXTRACTING {category} NETNAME{' ':<{title_spacing}}\n{'IDX':<{index_spacing}} {category:<{ip_spacing}} {'ISP/NETNAME':<{ip_spacing}}")

	for count, network in enumerate(networks):
		if "N/A" in network: network_netname.append("N/A")
		else:
			parsed_network = network.strip().split("/")[0]
			print(f"{success_style}{count+1:<{index_spacing}} {network:<{ip_spacing}} {sub_style}Checking for Last BGP Netname/ISP", end="\r", flush=True)
			
			session = requests.Session()
			retry = Retry(connect=3, backoff_factor=0.5)
			adapter = HTTPAdapter(max_retries=retry)
			session.mount('http://', adapter)
			session.mount('https://', adapter)
			
			response = session.get(target_url + parsed_network, headers=headers)
			data = response.text
			try:
				network_ip = [line for line in data.split('\n') if "descr:" in line or "Descr:" in line][0]
				parsed_netname = network_ip.split(":")[1].strip()
				network_netname.append(parsed_netname)
				print(f"{success_style}{count+1:<{index_spacing}} {network:<{ip_spacing}} {parsed_netname:<{end_spacing}}")
			except: continue
	time.sleep(timeout_count)
	return network_netname

def extract_final_hop(bgp_network):
	alive_addresses = list()
	last_hops = list()
	hops = list()
	print(f"{title_style}\n{'>> ':<{title_spacing}}EXTRACTING PINGABLE IPs PER SUBNET{' ':<{title_spacing}}\n{'IDX':<{index_spacing}} {'BGP IP':<{ip_spacing}} {'PINGABLE IP':<{ip_spacing}}")
	for count, bgp_prefix in enumerate(bgp_network):
		isAlive = False
		print(f"{' ':<{index_spacing}} {bgp_prefix:<{ip_spacing}} {sub_style}Checking for Pingable IPs", end="\r", flush=True)
		try:
			command = f"timeout 35s fping -a -g -q {bgp_prefix}"
			process = os.popen(command)
			for line in process:
				if line is not None:
					isAlive = True
					alive_addresses.append(line.split(" ")[0].strip())
					break
			if not isAlive: 
				alive_addresses.append("N/A")
		except: continue
		print(f"{success_style}{count+1:<{index_spacing}} {bgp_prefix:<{ip_spacing}} {alive_addresses[count]:<{end_spacing}}")
	
	time.sleep(timeout_count)
	print(f"{title_style}\n{'>> ':<{title_spacing}}FINDING THE LAST HOP PER PINGABLE ADDRESS{' ':<{title_spacing}}\n{'IDX':<{index_spacing}} {'BGP IP':<{ip_spacing}} {'PINGABLE IP':<{ip_spacing}} {'LAST HOP':<{ip_spacing}}")
	for maincount, alive_ip in enumerate(alive_addresses):
		isValidHop = False
		if "N/A" in alive_ip: last_hops.append("N/A")
		else:
			try:
				dec_count = 2
				while isValidHop != True:
					hops = list()
					print(f"{' ':<{index_spacing}} {bgp_network[maincount]:<{ip_spacing}} {alive_ip:<{ip_spacing}} {sub_style}Checking for Last Hop", end="\r", flush=True)
					command = f"mtr -r -n -c 1 {alive_ip}"
					process = os.popen(command)
					for line in process: hops.append(line)
					for count, line in enumerate(hops):
						if enableDebugMessage == True: print(f"\nCOUNT:{count} LENHOP:{len(hops)} DEC:{dec_count} HOP:{line}")
						if count == len(hops)-dec_count:
							extracted_hop = line.split("-- ")[1].split(" ")[0].strip()
							if "???" in line:
								print(f"{error_style}{maincount+1:<{index_spacing}} {bgp_network[maincount]:<{ip_spacing}} {alive_ip:<{ip_spacing}} ERROR: {extracted_hop} NULL VALUE{' ':<{ip_spacing}}")
								dec_count += 1
								isValidHop = False
							elif IP(extracted_hop).iptype() != "PUBLIC":
								print(f"{error_style}{maincount+1:<{index_spacing}} {bgp_network[maincount]:<{ip_spacing}} {alive_ip:<{ip_spacing}} ERROR: {extracted_hop} NOT PUBLIC IP{' ':<{ip_spacing}}")
								dec_count += 1
								isValidHop = False
							else:
								last_hops.append(extracted_hop)
								isValidHop = True
			except: continue
		print(f"{success_style}{maincount+1:<{index_spacing}} {bgp_network[maincount]:<{ip_spacing}} {alive_ip:<{ip_spacing}} {last_hops[maincount]:<{ip_spacing}}")	
	time.sleep(timeout_count)
	return alive_addresses, last_hops
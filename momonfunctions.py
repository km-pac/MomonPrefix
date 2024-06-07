import requests, os

title_spacing = 10
index_spacing = 5
ip_spacing = 25

class ExtractedIP:
	def	__init__(self, client_ip, bgp_network, isp_netname):
		self.client_ip = client_ip
		self.bgp_network = bgp_network
		self.isp_netname = isp_netname

	def pingnet(self):
		print(f"Conducting fping for {self.bgp_network}")
		os.system(f"fping -g {self.bgp_network}")

def extract_parse_clients(file_path):
	with open(file_path, 'r') as file: 
		lines = file.readlines() 
		extracted_ips = [line.strip() for line in lines]
		unique_ips = sorted(list(set(extracted_ips)))
		print(f"EXTRACTED CLIENT IPs: {len(extracted_ips)}\nUNIQUE CLIENT IPs: {len(unique_ips)}\n")
	return extracted_ips, unique_ips

def extract_bgp_network(target_url, headers, unique_ips):
	parsed_bgp_networks = list()
	bgp_networks = list()
	print(f"{' ':<{title_spacing}}EXTRACTING BGP NETWORK{' ':<{title_spacing}}\n\n{'IDX':<{index_spacing}} {'CLIENT IP':<{ip_spacing}} {'NETWORK/PREFIX LENGTH':<{ip_spacing}}")

	for count, ip in enumerate(unique_ips):
		response = requests.get(target_url + ip, headers=headers)
		data = response.text
		try: 
			client_ip = [line for line in data.split('\n') if "/net/" in line][0]
			parsed_network_ip = client_ip.strip().split("/net/")[1].split("\">")[0]
			parsed_bgp_networks.append(parsed_network_ip)
			print(f"{count+1:<{index_spacing}} {ip:<{ip_spacing}} {parsed_network_ip:<{ip_spacing}}")
		except: continue
		if count == 3: break
	bgp_networks = sorted(set(parsed_bgp_networks))
	print(f"\nEXTRACTED BGP NET: {len(parsed_bgp_networks)}\nUNIQUE BGP NET: {len(bgp_networks)}\n")
	return bgp_networks

def extract_bgp_netname(target_url, headers, bgp_networks):
	parsed_bgp_netname = list()
	bgp_netname = list()
	print(f"{' ':<{title_spacing}}EXTRACTING BGP NETNAME{' ':<{title_spacing}}\n\n{'IDX':<{index_spacing}} {'BGP IP':<{ip_spacing}} {'ISP/NETNAME':<{ip_spacing}}")

	for count, network in enumerate(bgp_networks):
		parsed_network = network.strip().split("/")[0]
		response = requests.get(target_url + parsed_network, headers=headers)
		data = response.text
		try:
			bgp_ip = [line for line in data.split('\n') if "netname:" in line or "NetName:" in line][0]
			parsed_bgp_netname = bgp_ip.split(":")[1].strip()
			bgp_netname.append(parsed_bgp_netname)
			print(f"{count+1:<{index_spacing}} {network:<{ip_spacing}} {parsed_bgp_netname:<{ip_spacing}}")
		except: continue
	return bgp_netname

def extract_final_hop(bgp_network):
	alive_addresses = list()
	last_hops = list()
	hops = list()
	print(f"\n{' ':<{title_spacing}}EXTRACTING PINGABLE IPs PER SUBNET{' ':<{title_spacing}}\n\n{'IDX':<{index_spacing}} {'BGP IP':<{ip_spacing}} {'PINGABLE IP':<{ip_spacing}}")
	for count, bgp_prefix in enumerate(bgp_network):
		isAlive = False
		print(f"{' ':<{index_spacing}} {bgp_prefix:<{ip_spacing}} Checking for Pingable IPs", end="\r", flush=True)
		try:
			command = f"fping -g {bgp_prefix}"
			process = os.popen(command)
			for line in process:
				if "alive" in line:
					isAlive = True
					alive_addresses.append(line.split(" ")[0].strip())
					break
			if not isAlive: 
				alive_addresses.append("N/A")
		except: continue
		print(f"{count+1:<{index_spacing}} {bgp_prefix:<{ip_spacing}} {alive_addresses[count]:<{50}}")

	print(f"\n{' ':<{title_spacing}}FINDING THE LAST HOP PER PINGABLE ADDRESS{' ':<{title_spacing}}\n\n{'IDX':<{index_spacing}} {'BGP IP':<{ip_spacing}} {'PINGABLE IP':<{ip_spacing}} {'LAST HOP':<{ip_spacing}}")
	for count, ip in enumerate(alive_addresses):
		isValidHop = False
		if "N/A" in ip: last_hops.append("N/A")
		else:
			try:
				while isValidHop != True:
					print(f"{' ':<{index_spacing}} {bgp_network[count]:<{ip_spacing}} {ip:<{ip_spacing}} Checking for Last Hop", end="\r", flush=True)
					command = f"mtr -r -n -u {ip}"
					process = os.popen(command)
					for line in process: hops.append(line)
					for count, line in enumerate(hops):
						if count == len(hops)-2: 
							if "???" in line: isValidHop = False
							else:
								isValidHop = last_hops.append(line.split("-- ")[1].split(" ")[0].strip())
								isValidHop = True
			except: continue
			print(f"{count+1:<{index_spacing}} {bgp_network[count]:<{ip_spacing}} {ip:<{ip_spacing}} {last_hops[count]:<{ip_spacing}}")

	
	
	return alive_addresses


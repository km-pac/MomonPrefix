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
		print(f"EXTRACTED CLIENT IPs: {len(extracted_ips)}\nUNIQE CLIENT IPs: {len(unique_ips)}\n")
	return extracted_ips, unique_ips

def extract_bgp_network(target_url, headers, unique_ips):
	parsed_bgp_networks = list()
	bgp_networks = list()
	print(f"{' ':<{title_spacing}}EXTRACTING BGP NETWORK{' ':<{title_spacing}}\n\n{'IDX':<{index_spacing}} {'CLIENT IP':<{ip_spacing}} {'NETWORK/PREFIX LENGHT':<{ip_spacing}}")

	for count, ip in enumerate(unique_ips):
		response = requests.get(target_url + ip, headers=headers)
		data = response.text
		try: 
			client_ip = [line for line in data.split('\n') if "/net/" in line][0]
			parsed_network_ip = client_ip.strip().split("/net/")[1].split("\">")[0]
			parsed_bgp_networks.append(parsed_network_ip)
			print(f"{count+1:<{index_spacing}} {ip:<{ip_spacing}} {parsed_network_ip:<{ip_spacing}}")
		except: continue
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
			print(f"{count+1:<5} {network:<25} {parsed_bgp_netname:<25}")
		except: continue
	return bgp_netname
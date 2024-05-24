import requests, os

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
	return extracted_ips, unique_ips

def extract_bgp_network(unique_ips):
	bgp_networks = list()
	target_url = "https://bgp.he.net/ip/"
	headers = {
    	'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build\\/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
	}

	for ip in unique_ips:
		response = requests.get(target_url + ip, headers=headers)
		data = response.text

		# try:
		client_ip = [line for line in data.split('\n') if "/net/" in line][0]
		bgp_networks.append(client_ip.strip().split("/net/")[1].split("\">")[0])
		print(bgp_networks)
		# except: continue

		return bgp_networks


# def extract_network(unique_ips):
	# ip_objs = list()
	# target_url = "https://bgp.he.net/ip/"
	# headers = {
    # 	'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build\\/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
	# 	}

	# for count, ip in enumerate(unique_ips):
	# 	response = requests.get(target_url + ip, headers=headers)
	# 	data = response.text
	
	# 	try: 
	# 		client_ip = [line for line in data.split('\n') if "/net/" in line][0]
	# 		netnames = [line for line in data.split('\n') if "netname:" in line or "NetName:" in line][0]	
	# 		parsed_ip = client_ip.strip().split("/net/")[1].split("\">")[0]
	# 		parsed_netname = netnames.split(":")[1].strip()
	# 	except: continue

	# 	ext_ips = ExtractedIP(ip, parsed_ip, parsed_netname)
	# 	print(f"{count+1:<10} {ip:<20} {ext_ips.bgp_network:<25} {ext_ips.isp_netname:<20}")

	# 	ip_objs.append(ext_ips)
	# return ip_objs


# bgp_networks = list()


# print(f"EXTRACTED CLIENT IP COUNT: {len(extracted_ips)} \nUNIQUE CLIENT IP COUNT: {len(unique_ips)}\n")
# print(f"{'INDEX':<10} {'CLIENT IP':<20} {'NETWORK/PREFIX LENGHT':<25} {'ISP':<20}")

# pubip_objs = extract_network(unique_ips)

# for obj in pubip_objs:
# 	bgp_networks.append(obj.bgp_network)

# bgp_networks = sorted(set(bgp_networks))

# print(f"\n\nNETWORK COUNT: {len(pubip_objs)} \nUNIQUE NETWORK COUNT: {len(bgp_networks)}\n")
# for count, bgp_networks in enumerate(bgp_networks):
# 	print(bgp_networks)

# export_bgp(bgp_networks)
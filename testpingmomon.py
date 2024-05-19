import requests, os
from tabulate import tabulate

class ExtractedIP:
	def	__init__(self, bgp_network, isp_netname):
		self.bgp_network = bgp_network
		self.isp_netname = isp_netname

	def pingnet(self):
		os.system(f"fping -g {self.bgp_network}")

def extract_network_netname(unique_ips):
	ip_objs = list()
	target_url = "https://bgp.he.net/ip/"
	headers = {
    	'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build\\/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
		}

	for count, ip in enumerate(unique_ips):
		response = requests.get(target_url + ip, headers=headers)
		data = response.text
	
		try: 
			client_ip = [line for line in data.split('\n') if "/net/" in line][0]
			netnames = [line for line in data.split('\n') if "netname:" in line or "NetName:" in line][0]	

			parsed_ip = client_ip.strip().split("/net/")[1].split("\">")[0]
			parsed_netname = netnames.split(":")[1].strip()
		except: continue

		ext_ips = ExtractedIP(parsed_ip, parsed_netname)
		print(f"{count+1:<10} {ip:<20} {ext_ips.bgp_network:<20} {ext_ips.isp_netname:<20}")

		ip_objs.append(ext_ips)

		if count == 10: return ip_objs


file_path = "clientips.txt"
with open(file_path, 'r') as file: 
	lines = file.readlines() 
	extracted_ips = [line.strip() for line in lines]
	unique_ips = set(extracted_ips)

os.system("clear")

print(f"EXTRACT COUNT: {len(extracted_ips)} \nUNIQUE COUNT: {len(unique_ips)}")
ip_objs = extract_network_netname(unique_ips)

for obj in ip_objs:
	print({obj.bgp_network})
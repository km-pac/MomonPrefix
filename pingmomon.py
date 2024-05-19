import requests, os
from tabulate import tabulate

bgp_peer = []
bgp_isp = []

target_url = "https://bgp.he.net/ip/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build\\/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
}

file_path = "clientips.txt"
with open(file_path, 'r') as file: 
	lines = file.readlines() 
	extracted_ips = [line.strip() for line in lines]
	unique_ips = set(extracted_ips)

print(f"{unique_ips}\n")
os.system("clear")

print(f"EXTRACT COUNT: {len(extracted_ips)} \nUNIQUE COUNT: {len(unique_ips)}")
for count, ip in enumerate(unique_ips):
	response = requests.get(target_url + ip, headers=headers)
	data = response.text
	
	try: 
		ips = [line for line in data.split('\n') if "/net/" in line][0]
		netnames = [line for line in data.split('\n') if "netname:" in line or "NetName:" in line][0]	
		parsed_ip = ips.strip().split("/net/")[1].split("\">")[0]
		parsed_netname = netnames.split(":")[1].strip()
	except: continue

	if count == 0: print(f"{'Index':<10} {'IP':<20} {'PARSED IP':<20} {'ISP':<20}")	
	print(f"{count+1:<10} {ip:<20} {parsed_ip:<20} {parsed_netname:<20}")

	bgp_peer.append(parsed_ip)
	bgp_isp.append(parsed_netname)
	
parsed_bgp_peer = set(bgp_peer)
print(f"BGP COUNT: {len(bgp_peer)} \nPARSED BGP COUNT: {len(parsed_bgp_peer)}")

for count, ip in enumerate(bgp_peer):
	print(ip, bgp_isp[count])
print("\n")
for count, ip in enumerate(bgp_peer):
	print(ip)

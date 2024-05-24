<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from testpingmomon import bgp_networks
=======
from testpingmomon import *
>>>>>>> a98f8e8bcc131feb2dbf1189f609b6b3e9c9432f
=======
from testpingmomon.py import *
>>>>>>> 1ce3c78b959afeccc6f100f8cc0c9619c8cdf35f

bgp_network = export_bgp()
=======
import os
from testpingmomon import extract_parse_clients
from testpingmomon import extract_bgp_network

file_path = "clientips.txt"
os.system("clear")
extracted_ips, unique_ips = extract_parse_clients(file_path)

extract_bgp_network(unique_ips)
>>>>>>> 279eeeb2ba57be52b3b5c6cbbba738b7bc3efaf2

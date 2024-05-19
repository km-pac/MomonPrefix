file_path = "fullip.txt"
with open(file_path, 'r') as file:
        lines = file.readlines()
        client_ips = [line.strip() for line in lines]
unique_values = set(client_ips)

print(len(unique_values))

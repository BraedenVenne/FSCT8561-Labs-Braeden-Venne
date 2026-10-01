import socket
import nmap


scanner = nmap.PortScanner()
# While loop for target host input validation 
while True:
    target = input("Enter target host: ")

    try:
        target_ip = socket.gethostbyname(target)
        print(f"Scanning {target_ip}\n")
        break

    except socket.gaierror:
        print("Invalid hostname or IP address")

# While loop for start port input validation
while True:
    try:
        start_port = int(input("Enter start port: "))

        # Check if port is in range
        if 1 <= start_port <= 65535:
            break
        else:
            print("Invalid value: start port out of range (1 - 65535)")
    # Check if value is a number
    except ValueError:
        print("Invalid - input a valid number")

# While loop for end port input validation
while True:
    try:
        end_port = int(input("Enter end port: "))

        # Check if port is in range
        if end_port < 1 or end_port > 65535:
            print("Invalid value: end port out of range (1 - 65535)")

        # Check if end port is less than or equal to start port
        elif end_port <= start_port:
            print("Invalid entry, end port cannot be  than be less than or equal to start port")
        else:
            break
    # Check if value is a number
    except ValueError:
        print("Invalid - input a valid number")

# Run Nmap scan on target host and port range
scanner.scan(
    target,
    f"{start_port}-{end_port}"
    )

print("PORT\t\tSTATE\t\tSERVICE")

# Access the port data in the dictionary and print results
if target in scanner.all_hosts() and scanner[target]["tcp"]:
    for port, data in scanner[target]["tcp"].items():
        # Label service as unknown if data is empty
        if data["name"] == '':
            print(f"{port}\t\t{data["state"]}\t\tunknown")
        else:
            print(f"{port}\t\t{data["state"]}\t\t{data["name"]}")
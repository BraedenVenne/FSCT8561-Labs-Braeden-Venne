import socket

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

# Function for scanning the open ports
def scan_port(target, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(0.5)


    result = sock.connect_ex(
        (target, port)
    )

    sock.close()

    if result == 0:
        return True
    else:
        return False

# List that stores all the open ports
open_ports = []
closed_ports = []

for port in range(start_port, end_port + 1):
    if scan_port(target, port):
        open_ports.append(port)
    else:
        closed_ports.append(port)

# Output for the found ports
print(f"Target: {target}\n")
print(f"scanning TCP ports {start_port} - {end_port}\n")

# Check if there are any ports in the list, if not print none found
if len(open_ports) > 0:
    print("PORT\t\tSTATE\t\tSERVICE")
    for port in open_ports:
        # Try and except for checking the service the port belongs to if applicable
        try:
            service = socket.getservbyport(
                port,
                "tcp"
            )
        except OSError:
            service = "N/A"
        print(f"{port}\t\tOpen\t\t{service.upper()}")
    for port in closed_ports:
        print(f"{port}\t\tNot Open\tN/A")
    print("\nScan complete.")
    print(f"{len(open_ports)} open port(s) found.")
else:
    print("No open ports found in the selected range.")
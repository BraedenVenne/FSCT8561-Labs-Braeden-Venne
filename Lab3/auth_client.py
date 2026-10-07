import socket
from getpass import getpass

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect((HOST, PORT))

authenticated = False

# Username and password authentication loop
while not authenticated:
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    # Format and send AUTH command to server
    auth_message = f"AUTH|{username}|{password}"

    client_socket.send(
        auth_message.encode()
    )

    # Receive server response
    response = client_socket.recv(1024).decode()
    print("Server:", response)

    # If max failed attempts threshold is reached, block connection
    if "Authentication blocked" in response:
            print("Connection closed by server.")
            client_socket.close()
            exit()

    # Proceed to OTP stage if password verification succeeded
    if "OTP_REQUIRED" in response:
        break

# TOTP authentication loop
if "OTP_REQUIRED" in response:
    while True:
        client_otp = input("Enter your OTP: ")

        # Format and send OTP command  to server
        otp_message = f"OTP|{client_otp}" 
        client_socket.send(
            otp_message.encode()
        )

        # Receive server response
        response = client_socket.recv(1024).decode()
        print("Server:", response)

            # If max failed attempts threshold is reached, block connection
        if "Authentication blocked" in response:
            print("Connection closed by server.")
            client_socket.close()
            exit()

        # If TOTP is authenticated proceed to next stage
        if "ACCESS_GRANTED" in response:
            break

# Message loop
while True:
    message = input(
        "Enter message or type EXIT to leave: "
    )

    # Allow user to type 'EXIT' to end the connection
    if message.upper() == "EXIT":

        client_socket.send(
            "EXIT|".encode()
        )

        response = client_socket.recv(1024)

        print("Server:", response.decode())

        break

    # Format and send MSG command to server
    protocol_message = f"MSG|{message}"
    client_socket.send(
        protocol_message.encode()
    )

    # Receive resposne
    response = client_socket.recv(1024)

    print("Server:", response.decode())

# End the connection
client_socket.close()

print("Disconnected")

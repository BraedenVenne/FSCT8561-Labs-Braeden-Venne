import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

# Create the client socket
client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Connects to the server
client_socket.connect((HOST, PORT))

# Prompt user for their username
username = input("Enter your username: ")

# Create 'HELLO' message
hello_message = "HELLO|" + username

# Send username to the server
client_socket.send(
    hello_message.encode()
)

# Receive the welcome response from the server
response = client_socket.recv(1024)

print("Server:", response.decode())

# Handles messages received from the server
def handle_messages():
    while True:
        data = client_socket.recv(1024)

        if not data:
            break

        # Display received message
        print("\n" + data.decode())

# Create a thread to for received messages
receive_thread = threading.Thread(
    target = handle_messages
)

# Start the receiving thread
receive_thread.start()

# While loop that allows the client to send multiple messages
while True:

    message = input(
        "Enter message or type EXIT to leave: "
    )

    # Allows the client to leave / break the message loop
    if message.upper() == "EXIT":

        client_socket.send(
            "EXIT|".encode()
        )
        
        response = client_socket.recv(1024)

        print("Server:", response.decode())

        break

    protocol_message = "MSG|" + message

    client_socket.send(
        protocol_message.encode()
    )

# Close the client's connection
client_socket.close()

print("Disconnected")

import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
# Allows the server to reuse the same port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen(6)

print("Server is waiting for a connection...")

# List that stores all the connected clients
clients = []

# Function that handles the communication with clients
def handle_clients(client_socket, client_address):

    print("Connected by:", client_address)

    username = None
    connected = True

    # Loop that receives data from the client and does various validation checks
    while connected:

        try:
            data = client_socket.recv(1024)

            # Checks if client disconnected unexpectedly
            if not data:
                print("Client disconnected unexpectedly")
                break

            message = data.decode()

            print("Received:", message)

            # Checks if message contains '|'
            if "|" not in message:
                client_socket.send(
                    "ERROR|Invalid command format".encode()
                )
                continue

            # Splits the data into a command + content
            command, content = message.split("|", 1)

            # Handles the 'HELLO' command
            if command == "HELLO":
                # Checks if username was provided
                if content == "":
                    client_socket.send(
                        "ERROR|Username required".encode()
                    )
                else:
                    username = content
                    print("Username:", username)

                    client_socket.send(
                        "OK|Hello ".encode() + username.encode()
                    )

            # Handles the 'MSG' command
            elif command == "MSG":

                # Checks if client sent HELLO before sending a message
                if username is None:
                    client_socket.send(
                        "ERROR|HELLO required first".encode()
                    )

                # Checks if message is empty
                elif content == "":
                    client_socket.send(
                        "ERROR|Message cannot be empty".encode()
                    )

                # Checks if message is greater than 200 characters
                elif len(content) > 200:
                    client_socket.send(
                        "ERROR|Message too long".encode()
                    )

                else:
                    print(username + " says:", content)

                    # For loop allowing clients to send messages to each other
                    for client in clients:
                        if client != client_socket:
                            client.send((username + ": " + content).encode())

                    # client_socket.send(
                    #     ("OK|Message received from " + username).encode()
                    # )

            # HAndles the 'EXIT' command
            elif command == "EXIT":

                client_socket.send(
                    "OK|Goodbye".encode()
                )

                # Stops the connection loop
                connected = False

            # Handles unknown commands
            else:
                client_socket.send(
                    "ERROR|Unknown command".encode()
                )

        # Handles clients disconnecting unexpectedly
        except ConnectionResetError:
            print("Connection reset by client")
            break

    # Remove client from list
    if client_socket in clients:
        clients.remove(client_socket)

    # Close client socket
    client_socket.close()
    print("Client disconnected")

# While loop that allows for additional clients to connect simultaneously
while True:
    try:
        client_socket, client_address = server_socket.accept()

        # Add client to 'clients' list
        clients.append(client_socket)

        # Create new thread for the client
        client_thread = threading.Thread(
            target = handle_clients, 
            args = (client_socket, client_address)
            )

        # Starts the client thread
        client_thread.start()
        
    # allows you to end the loop to close the server with ctrl + c    
    except KeyboardInterrupt:
        print("Server closed")
        server_socket.close()
        break

import socket

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send OTP command right away without sending AUTH first
test_otp_message = "OTP|123456"
print("Sending:", test_otp_message)
client_socket.send(test_otp_message.encode())

response = client_socket.recv(1024).decode()
print("Server Response:", response)

client_socket.close()
import socketio

sio = socketio.Client()

# Event handler that triggers upon the initial connection event
@sio.event
def connect():
    print("Connection established!")

    # Prompt user for username upon connecting
    username = input("Enter your username: ")
    sio.emit('HELLO', {'content': username})
    while True:
        message = input(
            "Enter message or type EXIT to leave: "
        )

        if message.upper() == "EXIT":

            sio.emit('EXIT')
            sio.disconnect()
            break

        sio.emit('MSG', {'content': message})


# Event listener for "server_response" events from the server
@sio.on('server_response')
def handle_response(data):
    # Print server reply
    print("Server: ", data.get('status'), "| ", data.get('message'))

# Event handler that triggers when the client disconnects from the server
@sio.event
def disconnect():
    print('disconnected from server')

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:5000')
    sio.wait()
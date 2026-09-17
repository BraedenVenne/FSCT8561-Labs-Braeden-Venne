import socketio

sio = socketio.Client()

# Event handler that triggers upon the initial connection event
@sio.event
def connect():
    print("Connection established!")
    message = "Hello Server this is Braeden Venne"
    sio.emit('chat_message', {'message': message})

# Event listener for "server_response" events from the server
@sio.on('server_response')
def handle_response(data):
    # Print server reply
    print("Server replied:", data.get('reply'))

# Event handler that triggers when the client disconnects from the server
@sio.event
def disconnect():
    print('disconnected from server')

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:5000')
    sio.wait()
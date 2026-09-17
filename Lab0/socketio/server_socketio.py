import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

# Event handler that triggers when the client connects to the server
@sio.event
def connect(sid, environ):
    print("connect", sid)

# Event listener that handles 'chat_message' messages and sends reply
@sio.on('chat_message')
def handle_client(sid, data):
    print("Client says", data.get('message'))
    sio.emit('server_response', {'reply': 'Your message has been received Client!'}, room=sid)

# Event handler that triggers when the client disconnects from the server
@sio.event
def disconnect(sid):
    print("Client disconnected", sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)

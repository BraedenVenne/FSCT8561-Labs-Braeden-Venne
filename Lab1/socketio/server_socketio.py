import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

# Event handler that triggers when the client connects to the server
@sio.event
def connect(sid, environ):
    print("connect", sid)
    sio.save_session(sid, {'username': None})

# Event listener that handles the 'HELLO' command
@sio.on('HELLO')
def handle_hello(sid, data):
    username = data.get('content','').strip()
    if not username:
        sio.emit('server_response', {'status': 'ERROR', 'content': 'Username required'}, to=sid)

    # Update session state with the validated username
    sio.save_session(sid, {'username': username})
    print("Username:", username)
    sio.emit('server_response', {'status': 'HELLO', 'message': username}, to=sid)


# Event listener that handles the 'MSG' command
@sio.on('MSG')
def handle_msg(sid, data):
    # Retrieve the state/session for this specific client
    session = sio.get_session(sid)
    username = session.get('username')
    content = data.get('content', '')

    # Error responses that are sent to the client if triggered
    if username is None:
        sio.emit('server_response', {'status': 'ERROR', 'message':'Username required'}, to=sid)
    elif not content:
        sio.emit('server_response', {'status': 'ERROR', 'message': 'Message cannot be empty'}, to=sid)
    elif len(content) > 200:
        sio.emit('server_response', {'status': 'ERROR', 'message': 'Message too long'}, to=sid)
    # Success response that gets sent to client with the message
    else:
        print(username, "says: ", content)
        sio.emit('server_response', {'status': 'OK', 'message': 'Message received from ' + username}, to=sid)

# Event handler that triggers when the client disconnects from the server
@sio.event
def disconnect(sid):
    print("Client disconnected", sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)

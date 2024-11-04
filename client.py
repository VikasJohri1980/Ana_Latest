import socketio

local_sio = socketio.Client()
#remote_sio = socketio.Client()

@local_sio.event
def connect():
    print("Successfully connected to local Flask server")

@remote_sio.event
def connect():
    print("Successfully connected to remote server")

@local_sio.event
def connect_error(data):
    print("The connection to the local Flask server failed:", data)

@remote_sio.event
def connect_error(data):
    print("The connection to the remote server failed:", data)


print("Connecting to local server at http://127.0.0.1:5000")
local_sio.connect('http://127.0.0.1:5000')

print("Connecting to remote server at https://tts-vikas.msriva.com")
remote_sio.connect('https://tts-vikas.msriva.com')

@local_sio.on('text_msg_local')
def handle_local_text_msg(msg):
    print('Handler triggered for text_msg_local')
    print('Received local text message in client:', msg)
    #remote_sio.emit('text_msg', msg)
    #print('Emitted text_msg to remote server')

@remote_sio.on('processed_event')
def on_processed_event(data):
    print('Received processed event in client:', data)
    with open('output_audio.mp3', 'wb') as f:
        f.write(data['audio_event'])
    print('writing done')
    local_sio.emit('new_audio')
    print('new_audio event emitted from client')

if __name__ == '__main__':
    print('client started')
    local_sio.wait()

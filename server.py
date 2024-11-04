from flask import Flask, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/audio')
def get_audio():
    return send_file('output_audio.mp3', mimetype='audio/mpeg')

@socketio.on('connect')
def test_connect():
    print('Client connected to default namespace')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected from default namespace')

@socketio.on('text_msg')
def handle_message(msg):
    print('Received text_msg in server:', msg)
    emit('text_msg_local', msg)
    print('Emitted text_msg_local')

@socketio.on('new_audio')
def handle_new_audio():
    emit('new_audio', broadcast=True)
    print('new_audio event emitted')

if __name__ == '__main__':
    socketio.run(app, debug=True)

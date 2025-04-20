from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
import uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "defaultsecret")
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    session_id = str(uuid.uuid4())
    return render_template('pc.html', session_id=session_id)

@app.route('/phone/<session_id>')
def phone(session_id):
    return render_template('phone.html', session_id=session_id)

@socketio.on('send_text')
def handle_send_text(data):
    session_id = data['session_id']
    text = data['text']
    emit('receive_text', {'text': text}, to=session_id)

@socketio.on('join')
def on_join(data):
    session_id = data['session_id']
    join_room(session_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

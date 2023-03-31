from flask import Flask, jsonify, request, abort
from skpy import Skype, SkypeChats
from datetime import datetime
from functools import wraps
import urllib.request

app = Flask(__name__)

SKYPE_TOKEN_FILE = "token"

# Decorator for limiting the length of incoming requests
def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Send message to Skype chat
def send_to_skype(message, chat_url):
    url = 'https://skypenotification.s3.eu-central-1.amazonaws.com/token'
    filename = 'token'
    urllib.request.urlretrieve(url, filename)
    sk = Skype(connect=True)
    sk = Skype(tokenFile=SKYPE_TOKEN_FILE)
    sc = SkypeChats(sk)
    url = sc.urlToIds(chat_url)
    ch = sk.chats[url["id"]]
    ch.sendMsg(message)

# Generate message and send to Skype chat
def generate_message(task):
    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{task['message']}"
    send_to_skype(message, task['chat_url'])

# Create task and send message to Skype chat
@app.route('/tasks', methods=['POST'])
@limit_content_length(4 * 1024 * 1024 * 1024)
def create_task():
    if not request.json or 'chat_url' not in request.json or 'message' not in request.json:
        abort(400)
    task = {
        'chat_url': request.json['chat_url'],
        'message': request.json['message']
    }
    generate_message(task)
    return jsonify({'success': True}), 200

if __name__ == '__main__':     
    app.run(debug=True, host='0.0.0.0', port='8085')



from flask import Flask, request
from extensions import chats
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/messages", methods=['POST'])
def post_message():
    topic = request.json.get('topic')
    if not topic:
        return {'error': 'Chat topic not provided'}, 400

    message = request.json.get('message')
    if not message:
        return {'error': 'Message not provided'}, 400

    response = chats.post_message(topic, message)
    return {'response': response}

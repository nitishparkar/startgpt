from flask import Flask, request
from extensions import chats
from dotenv import load_dotenv
from entity_extractor import EntityExtractor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import os

load_dotenv()

app = Flask(__name__)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
db.init_app(app)


class Messages(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    streamchat_channel_id = db.Column(db.String)
    message_id = db.Column(UUID(as_uuid=True))
    message_text = db.Column(db.Text)
    streamchat_user_id = db.Column(db.String)
    message_created_at = db.Column(db.DateTime)
    message_updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())


with app.app_context():
    db.create_all()

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


@app.route("/messages/import", methods=['POST'])
def import_message():
    messages = request.json
    e = EntityExtractor(messages)

    return {'response': 'ok'}


@app.route("/streamchat/webhook", methods=['POST'])
def streamchat_webhook():
    print('webhook request:')
    print(dict(request.headers))
    print(request.json)
    print('-------')
    j = request.json

    message = Messages(
        streamchat_channel_id=j["channel_id"],
        message_id=j["message"]["id"],
        message_text=j["message"]["text"],
        message_created_at=j["message"]["created_at"],
        message_updated_at=j["message"]["updated_at"],
        streamchat_user_id=j["user"]["id"]
    )
    print(message)
    db.session.add(message)
    db.session.commit()

    return {'response': 'ok'}

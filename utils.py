import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import request, jsonify
import jwt
import os
from dotenv import load_dotenv
from functools import wraps



load_dotenv()

secret_key = os.getenv('SECRET_KEY')
sender_email = os.getenv('sender_email')
smtp_server = os.getenv('smtp_server')
smtp_port = os.getenv('smtp_port')
smtp_username = os.getenv('smtp_username')
smtp_password = os.getenv('smtp_password')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

def send_email(receiver_email):
    message_body = "This is a email sent from Estimation Tool to inform your account is varified and you can reset now"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Forget Password Mail'
    message.attach(MIMEText(message_body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)
    return (True, receiver_email)



from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


class EstimationDatabase:
    def __init__(self, collection):
        self.collection = collection
    def create_estimation(self, estimation_data):
        estimation_data['timestamp'] = datetime.utcnow()
        result = self.collection.insert_one(estimation_data)
        return result

    def read_estimation(self, estimation_id):
        return self.collection.find_one({'_id': ObjectId(estimation_id)})

    def update_estimation(self, estimation_id, new_data):
        result = self.collection.update_one({'_id': ObjectId(estimation_id)}, {'$set': new_data})
        return result.modified_count > 0

    def delete_estimation(self, estimation_id):
        result = self.collection.delete_one({'_id': ObjectId(estimation_id)})
        return result.deleted_count > 0

def confidence_level(data_cal):
    if data_cal <=4:
        return "low"
    elif data_cal <=6:
        return "medium"
    elif data_cal <=8:
        return "high"
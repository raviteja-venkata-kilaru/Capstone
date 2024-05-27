from flask import Flask, request, render_template, jsonify, request ,url_for
from pymongo import MongoClient
import jwt
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

from utils import *

app = Flask(__name__)

load_dotenv()

bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
client = MongoClient("mongodb://localhost:27017/")
db = client['Capstone']
User_Table = db['User']
Historical_Table = db["Historical_Table"]
estimationDatabase_crud = EstimationDatabase(Historical_Table)

# User_Table.create_index([('Email', 1)], unique=True)

@app.route('/api/register',methods = ['POST','GET'])
def register_user():
    print("<><><><><><><><><><><><><><><><><><><><><><>")
    print(request)
    if request.method == 'POST':
        user_data = request.json
        print('<<<<<<<<<<<<<<<<<<<<<<<<<',user_data)
        if not user_data['firstname'] and not user_data['lastname'] and not user_data['email'] and not user_data['password']:
            return jsonify({'error': 'Fill Every details please'})
        user = User_Table.find_one({'email':user_data['email']})
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>',user)
        if user:
            return jsonify({'error':'User Already There, Please LogIn'})
        user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        print(user_data['password'])
        result = User_Table.insert_one(user_data)
        print(result.inserted_id)
        if result.inserted_id:
            return jsonify({'message':'User Registration Successful,Please LogIn'})
    return render_template('registration.html')
    
@app.route('/',methods = ['GET','POST'])
def login_user():
    if request.method == 'POST':
        user_data = request.json
        if  not user_data['email'] and not user_data['password']:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            return jsonify({'error': 'Please enter Email or Password'})
        
        user = User_Table.find_one({'email': user_data['email']})
        if user and bcrypt.check_password_hash(user['password'], user_data['password']):
            token = jwt.encode({'username':user['firstname']+user['lastname']}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token,'message':'Successfully Login'}), 200
        else:
            return jsonify({'error': 'Invalid email or password'})
    else:
        return render_template('login.html')

@app.route('/api/forget_password',methods = ['GET','POST','PATCH'])
def forget_user():
    if request.method == 'POST':
        user_data = request.json
        if  not user_data['email']:
            return jsonify({'error': 'Please enter email_id to reset'})
        user = User_Table.find_one({'email': user_data['email']})
        if user:
            result = send_email(user_data['email'])
            if result[0]:
                email = {
                    'eamil':result[1]
                }
                return render_template("initiate.html",email = email)
        else:
            return jsonify({'error': 'Invalid email or password'})
    elif request.method == 'PATCH':
        user_data = request.json
        user = User_Table.find_one({'email': user_data['email']})
        user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        result = User_Table.insert_one(user_data)
        if result.insert_id:
            token = jwt.encode({'username':user['firstname']+user['lastname']}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token,'message':'Successfully Reseted the password'}), 200
        else:
            return jsonify({'error': 'Not Able to Update the Password'})
    else:
        return render_template("forget_password.html") 

@app.route('/api/submit_estimation', methods = ['GET','POST'])
@token_required
def submit_estimation():
    if request.method == 'POST':
        estimation_data = request.json
        print(estimation_data)
        historical_table = estimationDatabase_crud.create_estimation(estimation_data)
        return jsonify({'estimation_id': str(historical_table.inserted_id)}), 201
    else:
        return render_template("dashboard.html")
    



@app.route('/api/calculate_estimation', methods = ['GET','POST'])
@token_required
def calculate_estimation():
    if request.method == 'GET':
        historical_estimations = list(Historical_Table.find({}))
        for item in historical_estimations:
            item['_id'] = str(item['_id'])
        if len(historical_estimations):
            print(historical_estimations)
            return jsonify({'history':historical_estimations}),200
        else:
            return jsonify({'message':'There is No data In database to Search'}),200
    if request.method == 'POST':
        data = request.json
        complexity = data['Complexity']
        size = data['Size']
        typeoftask = data['typeOfTask']
        historical_data = Historical_Table.find({'complexity':complexity,'size':size,'type': typeoftask}) 
        data1 = list(historical_data)
        data_len = len(data1)
        if not data_len:
            return jsonify({'message':"There is no data in database please add Estimation and confidence"})
        size_values = {"small":  4, "medium":  6, "large":  8}
        cal_size=0
        for i in data1:
            for key,value in i.items():
                if key == "size":
                    cal_size += size_values[value]
        data_cal = cal_size / data_len
        return jsonify({'estimated_effort': data_cal,"confidence_level": confidence_level(data_cal)}), 200


if "__main__" == __name__:
    app.run(debug=True,port=5010)
from flask import Flask, request, render_template, jsonify, request ,redirect, url_for
from pymongo import MongoClient
import jwt
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

from utils import *

app = Flask(__name__)

load_dotenv()

bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
client = MongoClient("mongodb://localhost:27017/") # connecting to MongoDB
db = client['Capstone'] # creating Database
User_Table = db['User'] # creating collection for user to store his athentication details, but collection will reflect in databse when data stored
Historical_Table = db["Historical_Table"] # creating collection to store Task's, but collection will reflect in databse when data stored
estimationDatabase_crud = EstimationDatabase(Historical_Table)

# User_Table.create_index([('Email', 1)], unique=True)

@app.route('/api/register',methods = ['POST','GET'])
def register_user():
    '''This API will help user to register his account to access Estimation Tool'''
    if request.method == 'POST':
        user_data = request.json    
        if not user_data['firstname'] or not user_data['lastname'] or not user_data['email'] or not user_data['password']:
            return jsonify({'error': 'Fill Every details please'})
        user = User_Table.find_one({'email':user_data['email']})
        if user:
            return jsonify({'error':'User Already There, Please LogIn'})
        user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8') # here when user login we are encrypting his password using this function
        user_data['token'] = ''
        result = User_Table.insert_one(user_data)
        if result.inserted_id:
            return jsonify({'message':'User Registration Successful,Please LogIn'})
    return render_template('registration.html')
    
@app.route('/',methods = ['GET','POST'])
def login_user():
    '''This API will help user to login and after to access the Estimation Tool where we can estimate and submit user Task's'''
    if request.method == 'POST':
        user_data = request.json
        if  not user_data['email'] or not user_data['password']:
            return jsonify({'error': 'Please enter Email or Password'})
        user = User_Table.find_one({'email': user_data['email']})
        if user and bcrypt.check_password_hash(user['password'], user_data['password']): # Here I am checking the password which is user entered and with stored password in collection
            token = jwt.encode({'username':user['firstname']+user['lastname']}, app.config['SECRET_KEY'], algorithm='HS256')
            User_Table.update_one({'_id': user['_id']},{'$set': {'token':token}})
            return jsonify({'token': token,'message':'Successfully Login'}), 200
        else:
            return jsonify({'error': 'Invalid email or password'})
    else:
        return render_template('login.html')

@app.route('/api/open_initiate')
def open_initiate():
    '''this API is for redirecting to html page where user can set his new password'''
    return render_template('initiate.html')

@app.route('/api/forget_password',methods = ['GET','POST','PATCH'])
def forget_user():
    '''This API will help to reset user password with provided email and user can set new password'''
    if request.method == 'POST':
        user_data = request.json
        if  not user_data['email']:
            return jsonify({'error': 'Please enter email_id to reset'}),400
        user = User_Table.find_one({'email': user_data['email']})
        if user:
            # result = send_email(user_data['email']) # we need smtp server and port to send email
            result = (True,user_data['email'])
            if result[0]:
                return jsonify({'email' : result[1]}),200
        else:
            return jsonify({'error': 'Invalid email or password'}),401
    elif request.method == 'PATCH':
        user_data = request.json
        user = User_Table.find_one({'email': user_data['email']})
        user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        result = User_Table.update_one({'_id':user['_id']},{'$set':{'password':user_data['password']}})
        if result.acknowledged:
            token = jwt.encode({'username':user['firstname']+user['lastname']}, app.config['SECRET_KEY'], algorithm='HS256')
            User_Table.update_one({'_id':user['_id']},{'$set':{'token':token}})
            return jsonify({'token': token,'message':'Successfully Reseted the password'}), 200
        else:
            return jsonify({'error': 'Not Able to Update the Password'}),401
    else:
        return render_template("forget_password.html") 

@app.route('/api/submit_estimation', methods = ['POST'])
@token_required # this is for Athenticate the user logged in or not
def submit_estimation():
    '''This API will Help User to Submit the Task with Estimation, Confidence, Range'''
    if request.method == 'POST':
        estimation_data = request.json
        if type(estimation_data['Estimation']) == int:
            pass
        elif type(estimation_data['Estimation']) == str:
            estimation_data['Estimation'] = int(estimation_data['Estimation'])
        historical_table = estimationDatabase_crud.create_estimation(estimation_data)
        return jsonify({'estimation_id': str(historical_table.inserted_id)}), 201
        
    
@app.route('/api/open_dashboard')
def open_dashboard():
    '''This API for open dashboard page where we can create Task's'''
    return render_template("dashboard.html")

@app.route('/api/listViewAll')
def listViewAll():
    '''This API will user to see the Task's which is in database in table format'''
    historical_estimations = list(Historical_Table.find({}))
    for item in historical_estimations:
        item['_id'] = str(item['_id'])
    if len(historical_estimations):
        return render_template('listView.html',viewList=historical_estimations)
    
@app.route('/api/editDetails',methods=['GET','PATCH'])
def editDetails():
    '''this API will help User to DELETE task form database,EDIT and SAVE EDITED Task's in database'''
    if request.method == 'PATCH':
        data = request.json
        result = Historical_Table.update_one({'_id':ObjectId(data['id'])},{'$set':{'Task':data['Task'],'Complexity':data['Complexity'],'Size':data['Size'],'typeOfTask':data['typeOfTask'],'Note':data['Note'],'Estimation':data['Estimation'],'Confidence':data['Confidence'],'Estimation_range':data['Estimation_range']}})
        if result.acknowledged:
            return jsonify({'message':'Edited Successufully','update_id':data['id']})
    else:
        operation = request.args.get('operation')
        id = request.args.get('id')
        data = ObjectId(id)
        if operation == "EDIT":
            historical_data = Historical_Table.find_one({'_id': data})
            return render_template('editData.html',editableData = historical_data)
        else:
            result = Historical_Table.delete_one({'_id':data})
            if result:
                viewList = list(Historical_Table.find({}))
                for item in viewList:
                    item['_id'] = str(item['_id'])
                return render_template('listView.html',viewList = viewList)


@app.route('/api/calculate_estimation', methods = ['GET','POST'])
@token_required # this is for athentication
def calculate_estimation():
    '''this API will help user to calculate the Estimation, Confidence and Range based on Complexity, Size and Type Of Task which he entered'''
    if request.method == 'GET':
        historical_estimations = list(Historical_Table.find({}))
        for item in historical_estimations:
            item['_id'] = str(item['_id'])
        if len(historical_estimations):
            return jsonify({'history':historical_estimations}),200
        else:
            return jsonify({'message':'There is No data In database to Search'}),200
    if request.method == 'POST':
        data = request.json
        complexity = data['Complexity']
        size = str(data['Size'])
        typeoftask = data['typeOfTask']
        historical_data = Historical_Table.find({'Complexity':complexity,'Size':size,'typeOfTask': typeoftask}) 
        data_in_list = list(historical_data)
        if not data_in_list:
            return jsonify({'message':"Manually enter the Estimation and Confidence level"})
        estimates = [data['Estimation'] if 'Estimation' in data.keys() else 0 for data in data_in_list]
        if not estimates:
            return jsonify({'estimated_effort':1,"confidence_level":"low","estimated_effort_range":'0-0'})
        estimate_effort = sum(estimates)//len(estimates)
        cal_size=sum([(estimate-estimate_effort)**2 for estimate in estimates])
        var = cal_size/len(estimates)
        s_d = var**0.5 # standerd_deviation
        l_b = estimate_effort - s_d # lower_boundery
        h_b = estimate_effort + s_d # higher_boundary
        if s_d < 5: 
            confidence = 'low'
        elif s_d <10:
            confidence = 'medium'
        else:
            confidence = 'high'
        estimate_effort_range = f"{l_b}-{h_b}"
        return jsonify({'estimated_effort': estimate_effort,"confidence_level": confidence,"estimate_effort_range":estimate_effort_range}), 200


if "__main__" == __name__:
    app.run(debug=True,port=5000) # Here we are running the server in 5000 port
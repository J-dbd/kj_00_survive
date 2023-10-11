from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
   return render_template('click_start_date.html')

@app.route('/select_team')
def selectTeam():
   return render_template('select_team.html')

@app.route('/click_start_date.html')
def createTeam():
   return render_template('create_team.html')



@app.route('/api/list', methods=['GET'])
def getGroup():
   groups = list(db.group.find({}, {'_id: False'}).sort('name', -1))
   return jsonify({'result': 'success', 'group': groups})
   return render_template('select_team.html')

@app.route('/api/list', methods=['GET'])
def getGroup():
   groups = list(db.group.find({}, {'_id: False'}).sort('name', -1))
   return jsonify({'result': 'success', 'group': groups})


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/forgot_pwd')
def forgot_pwd():
    return render_template('forgot_pwd.html')

@app.route('/sign_in')
def sign_in():
   return render_template('sign_in.html')

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

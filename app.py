from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from pymongo import MongoClient
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os 
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

client = MongoClient('mongodb://jiwon:jungle@43.200.163.82', 27017)
db = client.jungle

@app.route('/')
def home():
   return render_template('select_team.html')


@app.route('/api/list', methods=['GET'])
def getGroup():
   groups = list(db.group.find({}, {'_id: False'}).sort('name', -1))
   print(groups)
   return jsonify({'result': 'success', 'group': groups})


@app.route('/login', methods=['POST','GET'])
def login():
   if request.method=='POST':
      id=request.form['id']
      pw=request.form['password']
      isUser=db['user'].find_one({'id':id})
      if isUser and isUser['password']==pw:#create jwt token
         payload={"user":id,
            "exp":datetime.utcnow()+timedelta(seconds=60*60*24)}
         token=jwt.encode(
            payload=payload,
            key=app.config['SECRET_KEY'],
            algorithm="HS256"
         )
         return jsonify({'result':'success',
                        'access_token':token})
      else:
         if isUser==None:
            msg="아이디가 존재하지 않습니다."
         elif isUser and isUser['password']!=pw:
            msg="비밀번호가 올바르지 않습니다."
         return jsonify({'result':'fail','reason':msg})
      
   else:
      return render_template('login.html')

@app.route('/forgot_pwd')
def forgot_pwd(): 
    return render_template('forgot_pwd.html')

@app.route('/sign_in')
def sign_in():
   return render_template('sign_in.html')

if __name__ == '__main__':
    app.run(debug=True)

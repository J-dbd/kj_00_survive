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

#아이디/비밀번호 찾기
@app.route('/forgot_pwd',methods=['GET','POST'])
def forgot_pwd(): 
   if request.method=='POST':
      name=request.form['name']
      email=request.form['email']
      isUser=db['user'].find_one({'name':name,'email':email})
      if isUser==None:
         msg='존재하지 않는 유저입니다. 이름 혹은 이메일을 다시 확인해주세요.'
         return jsonify({'result':'fail','reason':msg})
      else:
         user_id=isUser['id']
         return jsonify({'result':'success','user_id':user_id})
   else:
      return render_template('forgot_pwd.html')

#아이디 찾기   
@app.route('/find_id',methods=['GET','POST'])
def find_id(): 
   if request.method=='POST':
      name=request.form['name']
      email=request.form['email']
      isUser=db['user'].find_one({'name':name,'email':email})
      if isUser==None:
         msg='이름 혹은 이메일을 다시 확인해주세요.'
         return jsonify({'result':'fail','data':msg})
      else:
         user_id=isUser['id']
         name=isUser['name']
         data={'user_id':user_id,'name':name}
         return jsonify({'result':'success','data':data})
   else:
      return jsonify({'result':'fail','data':'nothing'})

#비밀번호 찾기 
@app.route('/find_pwd',methods=['GET','POST'])
def find_pwd(): 
   if request.method=='POST':
      id=request.form['id']
      name=request.form['name']
      email=request.form['email']
      isUser=db['user'].find_one({'id':id,'name':name,'email':email})
      if isUser==None:
         msg='아이디, 이름, 이메일을 다시 확인해주세요.'
         return jsonify({'result':'fail','data':msg})
      else:
         user_id=isUser['id']
         name=isUser['name']
         pwd=isUser['password']
         data={'user_id':user_id,'name':name,'password':pwd}
         return jsonify({'result':'success','data':data})
   else:
      return jsonify({'result':'fail','data':'nothing'})
      
#회원가입
@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
   if request.method=='POST':
      #print("request.form",request.form.to_dict())
      id=request.form['id']
      pw=request.form['password']
      name=request.form['name']
      email=request.form['email']
      db['user'].insert_one({
         'id':id,
         'password':pw,
         'name':name,
         'email':email,
      })
      return jsonify({'result':'success'})
   else:
      return render_template('login.html')
@app.route('/welcome')
def welcome():
   return render_template('welcome.html')
if __name__ == '__main__':
    app.run(debug=True)

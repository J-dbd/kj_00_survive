from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify

from pymongo import MongoClient,UpdateOne
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os 
from dotenv import load_dotenv
from bson.objectid import ObjectId

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, create_refresh_token,get_jwt
)


app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
MONGO_DB=os.getenv('MONGO_DB')
client = MongoClient(MONGO_DB, 27017)

db = client.jungle

def get_week_number(date_str):
    try:
        # 날짜 문자열을 datetime 객체로 변환
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        # 날짜로부터 해당 주차 계산
        week_number = date.isocalendar()[1]

        return week_number
    except ValueError:
        return "날짜 형식이 잘못되었습니다."


@app.route('/api/list', methods=['GET'])
def getGroup():
   groups = list(db.group.find({}, {'_id: False'}).sort('name', -1))
   print(groups)
   return jsonify({'result': 'success', 'group': groups})

#####################
#회원가입과 환영페이지 #
######################      
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

#환영페이지
@app.route('/pop')
def pop():
   return render_template('pop.html')

#############
# JWT Token #
#############
jwt=JWTManager(app)
#로그인, jwt 토큰 발급
@app.route('/login', methods=['POST','GET'])
def login():
   if request.method=='POST':
      id=request.form['id']
      pw=request.form['password']
      isUser=db['user'].find_one({'id':id})
      if isUser and isUser['password']==pw:#create jwt token
         name=isUser['name']
         additional_claims={
            'name':name,
         }
         expires_delta=timedelta(seconds=60*60*10)
         access_token = create_access_token(identity=id,additional_claims=additional_claims,expires_delta=expires_delta)
         #print("access_token",access_token)
         return jsonify({'result':'success',
                        'access_token':access_token})
      else:
         if isUser==None:
            msg="아이디가 존재하지 않습니다."
         elif isUser and isUser['password']!=pw:
            msg="비밀번호가 올바르지 않습니다."
         return jsonify({'result':'fail','reason':msg})
      
   else:
      return render_template('login.html')

#JWT토큰 검증 API
@app.route("/validator", methods=["GET"])
@jwt_required(optional=True)
def protected():
    # Access the identity of the current user with get_jwt_identity
   current_identity = get_jwt_identity()
   if current_identity:
      data=get_jwt()
      #print(data)
      data={'id':data['sub'],'name':data['name']}
      return jsonify({'result':"success",'data':data})
   else:
      msg='Signature has expired'
      return jsonify({'result':"fail",'data':msg})

@app.route("/test")
def test():
   return render_template("test.html")


@app.route('/logout',methods=[])   

##############
# ID/PW 찾기 #
##############

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

@app.route('/select_team')
def select_team():
   return render_template('select_team.html')




@app.route('/')
def home():
   return render_template('team_page.html')

@app.route('/select_team', methods=["POST"])
def selectTeam():
   return render_template('select_team.html')

@app.route('/create_team')
def createTeam():
   return render_template('create_team.html')

@app.route('/team_page')
def teamPage():
   return render_template('team_page.html')

@app.route('/api/getDate', methods=['GET'])
def getDate():
    target_team = list(db.target_team.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'target_team': target_team})

@app.route('/api/getTeam', methods=['GET'])
def getTeam():
    teams = list(db.team.find({}, {'_id': False}))
    print(list(db.team.find({}, {'_id': False})))
    sorted_teams = sorted(teams, key=lambda x: (x['week'], x['number']))
    print(sorted_teams)
    return jsonify({'result': 'success', 'teams': sorted_teams})

@app.route('/api/getTarget', methods=['GET'])
def getTarget():
    targets = list(db.target.find({}, {'_id': False}))
    sorted_targets = sorted(targets, key=lambda x: (x['target_date'], x['member_id']))
    return jsonify({'result': 'success', 'targets': sorted_targets})

@app.route('/api/postTeam', methods=['POST'])
def postTeam():
    received_number = request.form['number_give']
    received_start_date = request.form['start_date_give']
    received_end_date = request.form['end_date_give']

    start_data_list = received_start_date.split("/")
    end_data_list = received_end_date.split("/")

    translated_start_data = start_data_list[2] + "-" + start_data_list[0] + "-" + start_data_list[1]
    translated_end_data = end_data_list[2] + "-" + end_data_list[0] + "-" + end_data_list[1]

    date_str = '2023-10-10'

    start_week_number = get_week_number(date_str)
    present_week_number = get_week_number(translated_start_data)

    week = present_week_number - start_week_number

    # week 계산 함수 작성 필요
    insert_dict = {"number": int(received_number), "start_date": translated_start_data, "end_date": translated_end_data, "team_member": {}, "week": week}
    db.team.insert_one(insert_dict)
    return jsonify({'result': 'success'})

@app.route('/target_list')
def target_list():
    team = {"team_member": ['minkyu', 'chanu'], "start_date": "2023-10-10", "name": 3}

    data = list(db.target.find({}, {"_id":1, "member_id":1, "text":1, "state":1}))
    result = {}
    total_count = len(data)
    cnt = 0
    for item in data:
        if item['state'] == True:
            item['state'] = "checked"
            cnt += 1
        else:
            item['state'] = ""
        text_state = [item['text'], item['state'], item['_id']]
        if not result.get(item['member_id']):
            result[item['member_id']] = []
            result[item['member_id']].append(text_state)
        else:
            result[item['member_id']].append(text_state)
    print(result)

    percentage = cnt/total_count * 100
    datetime_str = "2023-10-11"
    date_format = '%Y-%m-%d'

    date_obj = datetime.strptime(datetime_str, date_format)

    print(date_obj)
    print(datetime.now())

    return render_template('target_list.html',result=result, percentage = percentage, now = datetime.now(), current = date_obj, member_id="kyumin", target_date="2023-10-11")

@app.route('/api/check', methods=['POST'])
def is_checked():
   obj_id = request.form['obj_id']
   state = request.form['state']
   print(obj_id)
   # tgt = list(db.target.find({"_id": ObjectId(obj_id)}));
   if state == "checked":
       db.target.update_one({"_id": ObjectId(obj_id)}, {"$set": {"state": False}})
   else:
       db.target.update_one({"_id": ObjectId(obj_id)}, {"$set": {"state": True}})

   rtn_val = {'result': 'success'}
   return jsonify(rtn_val)

@app.route('/api/add_new_target', methods=['POST'])
def create_new_target():
    _dict = {
        'member_id': request.form['member_id'],
        'target_date': request.form['target_date'],
        'text': request.form['text'],
        'state': False
    }
    print(_dict)
    db.target.insert_one(_dict)

    rtn_val = {'result': 'success'}
    return jsonify(rtn_val)

@app.route('/api/delete_target', methods=['POST'])
def delete_target():
    _dict = {
        '_id': ObjectId(request.form['obj_id'])
    }
    db.target.delete_one(_dict)

    rtn_val = {'result': 'success'}
    return jsonify(rtn_val)

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

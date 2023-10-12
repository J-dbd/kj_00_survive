from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId
import bcrypt, datetime
from datetime import datetime, date

app = Flask(__name__)

client = MongoClient('mongodb://minkyu:jungle@43.200.163.82',27017)
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

@app.route('/')
def login():
   return render_template('login.html')
#
@app.route('/select_team')
def select_team():
   return render_template('select_team.html')

@app.route('/forgot_pwd')
def forgot_pwd():
    return render_template('forgot_pwd.html')

@app.route('/sign_in')
def sign_in():
   return render_template('sign_in.html')

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
    sorted_teams = sorted(teams, key=lambda x: (x['week'], x['name']))
    print(sorted_teams)
    return jsonify({'result': 'success', 'teams': sorted_teams})

@app.route('/api/getTarget', methods=['GET'])
def getTarget():
    targets = list(db.target.find({}, {'_id': False}))
    sorted_targets = sorted(targets, key=lambda x: (x['target_date'], x['member_id']))
    return jsonify({'result': 'success', 'targets': sorted_targets})

@app.route('/api/postTeam', methods=['POST'])
def postTeam():
    received_name = request.form['name_give']
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
    insert_dict = {"name": int(received_name), "start_date": translated_start_data, "end_date": translated_end_data, "team_member": {}, "week": week}
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

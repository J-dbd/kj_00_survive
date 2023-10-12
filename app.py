from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from pymongo import MongoClient, UpdateOne
from bson.objectid import ObjectId
import bcrypt
from datetime import datetime, date

app = Flask(__name__)

client = MongoClient('mongodb://minkyu:jungle@43.200.163.82',27017)
db = client.jungle

# @app.route('/')
# def home():
#    return render_template('target_list.html')
#
@app.route('/select_team')
def selectTeam():
   return render_template('select_team.html')
#
# @app.route('/click_start_date.html')
# def createTeam():
#    return render_template('create_team.html')
#
#
#
# @app.route('/api/list', methods=['GET'])
# def getGroup():
#    groups = list(db.group.find({}, {'_id: False'}).sort('name', -1))
#    return jsonify({'result': 'success', 'group': groups})
#    return render_template('select_team.html')
#
# @app.route('/login')
# def login():
#     return render_template('login.html')
#
# @app.route('/forgot_pwd')
# def forgot_pwd():
#     return render_template('forgot_pwd.html')
#
# @app.route('/sign_in')
# def sign_in():
#    return render_template('sign_in.html')


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

@app.route('/target_team_list')
def target_team_list():
    team = {"team_member": ['minkyu', 'chanu'], "start_date": "2023-10-10", "name": 3}

    data = list(db.target.find({}, {"_id":0, "member_id":1, "text":1, "state":1}))
    result = {}
    total_count = len(data)
    cnt = 0
    for item in data:
        if item['state'] == True:
            item['state'] = "checked"
            cnt += 1
        else:
            item['state'] = ""
        text_state = [item['text'], item['state']]
        if not result.get(item['member_id']):
            result[item['member_id']] = []
            result[item['member_id']].append(text_state)
        else:
            result[item['member_id']].append(text_state)
    print(result)

    percentage = cnt/total_count * 100

    return render_template('target_list.html',result=result, percentage = percentage)


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

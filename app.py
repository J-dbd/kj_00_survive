from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from pymongo import MongoClient
import bcrypt

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

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

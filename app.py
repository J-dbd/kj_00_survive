import datetime
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient('mongodb://chanu:jungle@43.200.163.82:27017', 27017)
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
def home():
   return render_template('team_page.html')

@app.route('/select_team')
def selectTeam():
   return render_template('select_team.html')

@app.route('/create_team')
def createTeam():
   return render_template('create_team.html')

@app.route('/team_page')
def teamPage():
   return render_template('team_page.html')


@app.route('/api/getTeam', methods=['GET'])
def getTeam():
    teams = list(db.team.find({}, {'_id': False}))
    sorted_teams = sorted(teams, key=lambda x: (x['week'], x['name']))
    print(sorted_teams)
    return jsonify({'result': 'success', 'teams': sorted_teams})

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

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
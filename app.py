from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
   return render_template('select_team.html')

@app.route('/api/list', methods=['GET'])
def getGroup():
   groups = list(db.group.find({}, {'_id: False'}).sort('name', -1))
   return jsonify({'result': 'success', 'group': groups})


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

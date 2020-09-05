from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from datetime import datetime
from sqlalchemy import desc
from flask import render_template
import numpy as np
import sys

app=Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] ='postgres://brjgqjmnamwnxc:2038ec5ace178f7e6f34d1015384a39e7274126f60488b14a5403582ae5a8966@ec2-3-95-87-221.compute-1.amazonaws.com:5432/d3s7d1dsfli0sd'

app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
groupId=0
class usermessage(db.Model):
    __tablename__ ='usermessage'
    id = db.Column(db.String(50), primary_key=True)
    group_num = db.Column(db.Text)
    nickname = db.Column(db.Text)
    group_id = db.Column(db.String(50))
    type = db.Column(db.Text)
    status = db.Column(db.Text)
    account = db.Column(db.Text)
    user_id = db.Column(db.String(50))
    message = db.Column(db.Text)
    birth_date = db.Column(db.TIMESTAMP)



@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        userId = request.values['userId']
        SaveMsgNumber = usermessage.query.order_by(usermessage.birth_date).filter(usermessage.user_id==userId).filter(usermessage.status=='save').filter(usermessage.type=='user').count()
        data_SaveData = usermessage.query.order_by(usermessage.birth_date).filter(usermessage.user_id==userId).filter(usermessage.status=='save').filter(usermessage.type=='user')
        save_dic = {}
        save_list = []
        count=0
        for _Data in data_SaveData:
            count+=1
            save_dic['number'] = count
            save_dic['account'] = _Data.account
            save_dic['message'] = _Data.message
            save_list.append(save_dic)
            save_dic = {}

        add=0
        for i in range(SaveMsgNumber):
            try:
                money = int(save_list[i]['account'])
            except:
                money = int(0)
            add += money
        result = str(add)+'元'


        
        return render_template('index_form.html',**locals())

    return render_template('home.html',**locals())

@app.route('/submit',methods=['POST','GET'])
def submit():
    groupId = 0

    return groupId

if __name__ =="__main__":
    app.run()

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from datetime import datetime
from sqlalchemy import desc
from flask import render_template
import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import base64
from io import BytesIO

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
        food=0
        cloth=0
        sleep=0
        walk=0
        education=0
        play=0
        unknown=0
        for i in range(SaveMsgNumber):
            Message = save_list[i]['message']
            if "食/" in Message:
                food+= int(save_list[i]['account'])
            elif "衣/" in Message:
                cloth+= int(save_list[i]['account'])
            elif "住/" in Message:
                sleep+= int(save_list[i]['account'])
            elif "行/" in Message:
                walk+= int(save_list[i]['account'])
            elif "育/" in Message:
                education+= int(save_list[i]['account'])
            elif "樂/" in Message:
                play+= int(save_list[i]['account'])
            elif "其他/" in Message:
                unknown+= int(save_list[i]['account'])
            else:
                continue
            try:
                money = int(save_list[i]['account'])
            except:
                money = int(0)
            add += money
        result = str(add)+'元'

        plt.rcParams['figure.dpi'] = 200  # 分辨率
        plt.figure(facecolor='#FFEEDD',edgecolor='black',figsize=(2.5,1.875))
        plt.rcParams['savefig.dpi'] = 150  # 圖片像素
        #plt.rcParams["font.sans-serif"]= "Microsoft JhengHei"
        # plt.rcParams['figure.figsize'] = (1.5, 1.0)  # 设置figure_size尺寸800x400


        plt.rcParams["font.family"]="SimHei"
        data = [food,cloth,sleep,walk,education,play,unknown]
        category =['Food','Clothing','Housing',"Transportation",'Education','Entertainment','Others']
        color = ["red", "lightblue", "pink", "green", "orange","blue","purple"]
        # separeted = (0, 0, 0, 0, 0, 0)
        plt.pie(data,                            #資料數值
                labels = category,               #數值標籤
                autopct = "%.0f%%",              #數值百分比(留到百分比幾位)
                colors = color,                   #顏色
                # explode = separeted,             #是否有突出資料
                radius = 1.5,                    #半徑
                pctdistance = 0.65,              #數值與圓餅圖的圓心距離
                center = (-10,0),                #圓心座標
                textprops = {"fontsize" : 6},   #文字大小
                labeldistance = 1.6,             #標籤顯示位置
                shadow = False)                   #是否有陰影
        plt.axis('equal')      #讓圓餅圖比例相等           
        # plt.legend(loc = "center right")

        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        # 將matplotlib圖片轉換為HTML
        imb = base64.b64encode(plot_data)  # 對plot_data進行編碼
        ims = imb.decode()
        imd = "data:image/png;base64," + ims
        img = imd
        
        return render_template('index_form.html',**locals())

    return render_template('home.html',**locals())

@app.route('/submit',methods=['POST','GET'])
def submit():
    groupId = 0

    return groupId

if __name__ =="__main__":
    app.run()

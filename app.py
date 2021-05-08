from flask import Flask
from flask import json, request
from Train_Vecorize import b, c,Preprocess_Vectorize_TFIDF
from Train_RandomForest import e,RandomForest
from Train_MLR import MLR
from Predict_Text_Score import Predict_textScore
from Predict_MLR import Predict_Storypoint
from single_prefict_TS import single_prefict_TS
from single_predict_MLR import single_predict_MLR
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

CORS(app)
mysql = MySQL(app)

@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=="GET":
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
        firstName = "details['fname']"
        lastName = "details['lname']"
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        json={
            "name":"kelum",
            "num":c()
        }
        return json

@app.route('/developers',methods=["GET","POST"])
def developers():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM developer")
        devs=cur.fetchall()
        cur.close()
        # print(json.dumps( devs))
        return json.dumps( devs)
        
    elif request.method=="POST":
        jsont={
            "name":"kelum",
            "num":c()
        }
        return jsont

@app.route('/bugreport/<bugId>',methods=["GET"])
def bugreport(bugId):
    if request.method=="GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT b.Id,b.Summary,b.Description,b.StroyPoint,b.PredictedStoryPoint,bc.Comment,d.Name FROM bugdev bd JOIN developer d ON bd.DevId = d.Id RIGHT JOIN bug b ON b.Id = bd.BugId LEFT JOIN bugcomment bc ON b.Id = bc.BugId WHERE b.Id=%s;",[bugId])
        bugs=cur.fetchall()
        cur.close()
        bugList=[]
        names=[]
        comments=[]
        temp={}
        for result in bugs:
            temp={"Id":result[0],"Summary":result[1],"Description":result[2],"StroyPoint":result[3],"PredictedStoryPoint":result[4],"Comment":result[5],"Name":result[6]}
            bugList.append(temp)
            temp={}
        for bg in bugList:
            if bg["Comment"]!=None:
                if bg["Comment"] not in comments:
                    comments.append(bg["Comment"])
            if bg["Name"]!=None:
                if bg["Name"] not in names:
                    names.append(bg["Name"])
        bugList[0]["Comment"]=comments
        bugList[0]["Name"]=names
        # print(bugList[0])
        return {"bugreport":bugList}


@app.route('/bug',methods=["GET","POST"])
def bug():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        # cur.execute("SELECT b.Id,b.Summary,b.Description,b.StroyPoint,b.PredictedStoryPoint,bc.Comment,d.Name FROM bugdev bd JOIN developer d ON bd.DevId = d.Id RIGHT JOIN bug b ON b.Id = bd.BugId LEFT JOIN bugcomment bc ON b.Id = bc.BugId")
        cur.execute("SELECT * FROM bug")
        bugs=cur.fetchall()
        cur.close()
        # print(json.dumps( bugs))
        # return json.dumps( bugs)
        bugList=[]
        temp={}
        for result in bugs:
            temp={"Id":result[0],"Summary":result[1],"Description":result[2],"StroyPoint":result[3],"PredictedStoryPoint":result[4]}
            bugList.append(temp)
            temp={}
        # print(bug)
        return {"bugs":bugList}

    elif request.method=="POST":
        # print(request.json)
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO bug(Summary, Description) VALUES (%s, %s)", (request.json['summary'], request.json['description']))
            id=mysql.connection.insert_id()
            mysql.connection.commit()
            for devId in request.json['developers']:
                cur.execute("INSERT INTO bugdev(DevId, BugId) VALUES (%s, %s)", (devId, id))
            mysql.connection.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
        jsont={
            "name":"kelum",
            "num":c()
        }
        return jsont

@app.route('/train',methods=["GET","POST"])
def train():
    if request.method=="GET":
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
        Preprocess_Vectorize_TFIDF('./../dataset/spring.csv')
        Accuracy=RandomForest()
        Accuracy2=MLR()
        json={
            "name":"kelum",
            "num":e(),
            "accuracy":Accuracy,
            "accuracy2":Accuracy2
        }
        return json

@app.route('/predict',methods=["GET","POST"])
def predict():
    if request.method=="GET":
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
        Predict_textScore()
        Predict_Storypoint()
        json={
            "name":"predicted",
            "num":c()
        }
        return json

@app.route('/trainmodel',methods=["GET","POST"])
def trainmodel():
    if request.method=="GET":
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
        f = request.files['file']
        f.save(os.path.join("dataset/", secure_filename("data.csv")))
        Preprocess_Vectorize_TFIDF('./dataset/data.csv')
        Accuracy=RandomForest()
        Accuracy2=MLR()
        meassures={
            "AccuracyMeassures1":Accuracy,
            "AccuracyMeassures2":Accuracy2
        }
        print(Accuracy["Mean Squared Error"])
        cur = mysql.connection.cursor()
        cur.execute("UPDATE accuracy SET `Mean Absolute Error`=%s,`Mean Squared Error`=%s,`Root Mean Squared Error`=%s WHERE Id=1", (Accuracy["Mean Absolute Error"], Accuracy["Mean Squared Error"],Accuracy["Root Mean Squared Error"]))
        cur.execute("UPDATE accuracy SET `Mean Absolute Error`=%s,`Mean Squared Error`=%s,`Root Mean Squared Error`=%s WHERE Id=2", (Accuracy2["Mean Absolute Error"], Accuracy2["Mean Squared Error"],Accuracy2["Root Mean Squared Error"]))
        mysql.connection.commit()
        cur.close()
        return meassures

@app.route('/accuracy',methods=["GET","POST"])
def accuracy():
    if request.method=="GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM accuracy")
        acc=cur.fetchall()
        cur.close()
        meassures={
            "AccuracyMeassures1":{"Mean Absolute Error": acc[0][1], "Mean Squared Error": acc[0][2], "Root Mean Squared Error": acc[0][3]},
            "AccuracyMeassures2":{"Mean Absolute Error": acc[1][1], "Mean Squared Error":acc[1][2], "Root Mean Squared Error": acc[1][3]},
        }
        return meassures
        
    elif request.method=="POST":
        jsont={
            "name":"kelum",
            "num":c()
        }
        return jsont

@app.route('/storypointgen',methods=["GET","POST"])
def traineddata():
    if request.method=="GET":
        return "meassures"
        
    elif request.method=="POST":
        # print(request.json['bug']["Description"])
        data=request.json['bug']["Summary"],request.json['bug']["Description"],len(request.json['bug']["Name"]),len(request.json['bug']["Comment"]),request.json['bug']["Id"],request.json['bug']["StroyPoint"]
        # print(data)
        single_prefict_TS(data)
        sp = single_predict_MLR()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE bug SET `PredictedStoryPoint`=%s WHERE Id=%s", (sp, request.json['bug']["Id"]))
        mysql.connection.commit()
        cur.close()
        jsont={
            "Predicted":sp
        }
        return jsont

@app.route('/comment',methods=["GET","POST","DELETE"])
def comment():
    if request.method=="GET":
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bugcomment(BugId, Comment) VALUES (%s, %s)", (request.json['Id'], request.json['comment']))
        mysql.connection.commit()
        cur.close()
        return "Comment saved"
    elif request.method=="DELETE":
        print(request.json['bugId'])
        print(request.json['comment'])
        return "comment deleted!"

@app.route('/deletecomment',methods=["GET","POST"])
def deletecomment():
    if request.method=="GET":
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
        print(request.json['bugId'])
        print(request.json['comment'])
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM bugcomment WHERE BugId=%s AND Comment=%s", (request.json['bugId'], request.json['comment']))
        mysql.connection.commit()
        cur.close()
        return "comment deleted!"

@app.route('/deletebug',methods=["GET","POST"])
def deletebug():
    if request.method=="GET":
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
        print(request.json['bugId'])
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM bug WHERE Id=%s", (str(request.json['bugId'])))
        mysql.connection.commit()
        cur.close()
        return "bug deleted!"

import Train_Vecorize  
import Train_RandomForest
import Train_MLR 
import Predict_Text_Score
import Predict_MLR
import json
import json
import os
import pandas as pd

if __name__== '__main__':
    app.run(debug=True)
from flask import Flask
from flask import json, request
from Train_Vecorize import b, c,Preprocess_Vectorize_TFIDF
from Train_RandomForest import e,RandomForest
from Train_MLR import MLR
from Predict_Text_Score import Predict_textScore
from Predict_MLR import Predict_Storypoint
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.utils import secure_filename

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
        print(json.dumps( devs))
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
        cur.execute("SELECT b.Id,b.Summary,b.Description,b.StroyPoint,b.PredictedStoryPoint,bc.Comment,d.Name FROM bugdev bd JOIN developer d ON bd.DevId = d.Id RIGHT JOIN bug b ON b.Id = bd.BugId LEFT JOIN bugcomment bc ON b.Id = bc.BugId WHERE b.Id=%s;",(bugId))
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
        print(bugList[0])
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
        print(bug)
        return {"bugs":bugList}

    elif request.method=="POST":
        print(request.json)
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
        Preprocess_Vectorize_TFIDF()
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
        f.save(os.path.join('dataset', secure_filename(f.filename)))
        return 'file uploaded successfully'

import Train_Vecorize  
import Train_RandomForest
import Train_MLR 
import Predict_Text_Score
import Predict_MLR
import json
import json
import os

if __name__== '__main__':
    app.run(debug=True)
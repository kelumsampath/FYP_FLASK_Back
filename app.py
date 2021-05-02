from flask import Flask
from flask import request
from Train_Vecorize import b, c,Preprocess_Vectorize_TFIDF
from Train_RandomForest import e,RandomForest
from Train_MLR import MLR
from Predict_Text_Score import Predict_textScore
from Predict_MLR import Predict_Storypoint
from flask_mysqldb import MySQL
from flask_cors import CORS
import json


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

@app.route('/bug',methods=["GET","POST"])
def bug():
    if request.method=="GET":
        print('ss')
        return 'Hello, World!'+str(b())
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
        json={
            "name":"kelum",
            "num":c()
        }
        return json

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

import Train_Vecorize  
import Train_RandomForest
import Train_MLR 
import Predict_Text_Score
import Predict_MLR

if __name__== '__main__':
    app.run(debug=True)
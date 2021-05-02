from flask import Flask
from flask import request
from Train_Vecorize import b, c,Preprocess_Vectorize_TFIDF
from Train_RandomForest import e,RandomForest
from Train_MLR import MLR
from Predict_Text_Score import Predict_textScore
from Predict_MLR import Predict_Storypoint
from flask_mysqldb import MySQL
from flask_cors import CORS


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

@app.route('/bug',methods=["GET","POST"])
def bug():
    if request.method=="GET":
        print('ss')
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
        print(request.json)
        print('sssssssss')
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
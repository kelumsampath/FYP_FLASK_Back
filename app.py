from flask import Flask
from flask import request
from Train_Vecorize import b, c,Preprocess_Vectorize_TFIDF
from Train_RandomForest import e,RandomForest
from Train_MLR import MLR
from Predict_Text_Score import Predict_textScore
from Predict_MLR import Predict_Storypoint

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=="GET":
        return 'Hello, World!'+str(b())
    elif request.method=="POST":
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
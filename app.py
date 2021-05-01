from flask import Flask
from flask import request
from user import b, c

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

import user   

if __name__== '__main__':
    app.run(debug=True)
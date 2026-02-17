import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3
import pandas as pd

import warnings

import sqlite3
import random

import smtplib 
from email.message import EmailMessage
from datetime import datetime

warnings.filterwarnings('ignore')



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about1():
    return render_template("about.html")


@app.route('/logon')
def logon():
	return render_template('register.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("login.html")

    


@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("login.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home.html")
    else:
        return render_template("login.html")

@app.route("/notebook")
def notebook1():
    return render_template("Notebook.html")


@app.route('/predict',methods=['POST'])
def predict():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model.sav')
    predict = model.predict(final4)

    if predict == 0:
        output = "INSOMNIA IS A COMMON SLEEP DISORDER THAT CAN MAKE IT HARD TO FALL ASLEEP OR STAY ASLEEP!" 
    elif predict == 1:
        output = "NONE, PATIENT IS NOT SUFFERS FROM SLEEP DISORDER!" 
    elif predict == 2:
        output = "SLEEP APNEA IS A POTENTIALLY SERIOUS SLEEP DISORDER IN WHICH BREATHING REPEATEDLY STOPS AND STARTS!" 
    
    return render_template('prediction.html', output=output)



if __name__ == "__main__":
    app.run(debug=False)

from flask import Blueprint,request,jsonify, current_app
import smtplib
from email.message import EmailMessage
import random
import re as RegularExpression
import MySQLdb

signup_bp = Blueprint('signup', __name__)
OTP = {}

@signup_bp.route('/signup', methods=["POST"])
def signup() :
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(RegularExpression.fullmatch(string=email,pattern=regex)):
        
        var = submitdata(name,email,password)
        if(var):
            sendOTP(email)
            return jsonify({"success" : True,"message": "OTP sent to " +email}), 200
        else :
            return jsonify({"success" : False,"message": "Email already taken"}), 200
    else:
       return jsonify({"success" : False ,"message": "Email Invalid" ,}), 400
    
def submitdata(name,email,password):
    from app import mysql

    try: 
    # Execute a SQL query to select all rows from the 'users' table
        cursor = mysql.connection.cursor()
        sql = "Insert into users (name,email,password) VALUES (%s, %s, %s)"
        val = (name,email,password)
        cursor.execute(sql,val)
        mysql.connection.commit()
        cursor.close()
        return True
    except MySQLdb._exceptions.IntegrityError:
        print("error")
        return False


def sendOTP(email):
    global OTP
    otp = random.randint(100000, 999999)
    OTP[email] = otp
    data = smtplib.SMTP("smtp.gmail.com",587)
    data.starttls()
    data.login(current_app.config["email"],current_app.config["password"])
    msg = EmailMessage()
    msg['Subject'] = "Email verification Required"
    msg['From'] = current_app.config["email"]
    msg['To'] = email
    msg.set_content("Your OTP for email verification is " + str(otp))
    data.send_message(msg)
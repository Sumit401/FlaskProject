import random
import re as RegularExpression
import smtplib
from email.message import EmailMessage

from firebase_admin import firestore
from flask import Blueprint, current_app, jsonify, request

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
        if(var)  :
            sendOTP(email)
            return jsonify({"success" : True,"message": "OTP sent to " +email}), 200
        else :
            return jsonify({"success" : False,"message": "Email already taken"}), 200
    else:
       return jsonify({"success" : False ,"message": "Email Invalid" ,}), 400
    
def submitdata(name,email,password):
    try:
        user_ref = firestore.client().collection("users")
        document_ref = user_ref.document(email.lower())
        document_snapshot = document_ref.get()
        if document_snapshot.exists:
            return False
        else:
            documents = user_ref.stream()
            total_documents = 0
            for document in documents:
                total_documents += 1
            user_ref.document(email).set({"id" : total_documents+1,"email" : email, "name" : name, "password" : password, "verifiedAt" : None, "token" : None})
        return True
    except Exception as e:
        print(e)
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
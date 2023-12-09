from flask import Blueprint,request,jsonify
import smtplib
from email.message import EmailMessage
import math, random
import re

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=["POST"])
def signup() :
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(string=email,pattern=regex)):
        digits = "0123456789"
        OTP = ""
    
    # length of password can be changed
    # by changing value in range
        for i in range(6) :
            OTP += digits[math.floor(random.random() * 10)]

        
        data = smtplib.SMTP("smtp.gmail.com",587)
        data.starttls()
        data.login("sumitsinha401@gmail.com","lykv hsdo nsyb mnrj")
        msg = EmailMessage()
        msg['Subject'] = "OTP from Sumit"
        msg['From'] = "sumitsinha401@gmail.com"
        msg['To'] = email
        msg.set_content("Your otp for email verification is " + OTP)
        print("mail sent")
        data.send_message(msg) 
        return jsonify({"success" : True,"message": "OTP sent to " +email}), 200
    else:
       return jsonify({"success" : False ,"message": "Email Invalid" ,}), 400



    
    
    
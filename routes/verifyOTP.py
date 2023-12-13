from flask import Blueprint,jsonify, request,current_app
from .signup import OTP
import datetime
import jwt
from datetime import datetime, timedelta

verifyOTP_bp = Blueprint('verifyotp', __name__)

@verifyOTP_bp.route('/verifyotp', methods=["POST"])
def verifyotp():
    email = request.form["email"]
    otp = request.form["otp"]
    global OTP

    if str(OTP) == "{}":
        return jsonify({"success" : False,  "data" : "Incorrect OTP",})
    elif (str(OTP[email]) == otp) :
        token = submitdata(email)
        return jsonify({"success" : True, "data" : "OTP verified successfully", "token" : token})
    else:
        return jsonify({"success" : False,  "data" : "Incorrect OTP",})
    

def submitdata(email):
    from app import mysql
    cursor = mysql.connection.cursor()
    
    sql = "Update users set verifiedAt = (%s) where email = (%s)"
    val = (datetime.now(),email)
    cursor.execute(sql,val)
    cursor.close()
    mysql.connection.commit()
    cursor2 = mysql.connection.cursor()
    sql1 = "SELECT id FROM `users` WHERE email = (%s)"
    val1 = (email,)
    cursor2.execute(sql1, val1)
    data = cursor2.fetchall()
    cursor2.close()
    cursor3 = mysql.connection.cursor()
    token = jwt.encode(payload={"data" : {
                    "email" : email,
                    "id" : data[0][0]
                }, "exp" : (datetime.utcnow() + timedelta(minutes=10))},key=current_app.config['secretKey'],)
    
    sql2 = "Update users set token = (%s) where email = (%s)"
    val2 = (token,email,)
    cursor3.execute(sql2,val2)
    cursor3.close()
    mysql.connection.commit()
    return token
    

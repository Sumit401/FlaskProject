from flask import Blueprint,jsonify, request
from .signup import OTP
import datetime
verifyOTP_bp = Blueprint('verifyotp', __name__)

@verifyOTP_bp.route('/verifyotp', methods=["POST"])
def verifyotp():
    
    email = request.form["email"]
    otp = request.form["otp"]
    global OTP

    if(str(OTP[email]) == otp):
        submitdata(email)
        return jsonify({"success" : True, "data" : "OTP verified successfully"})
    else:
        return jsonify({"success" : False,  "data" : "Incorrect OTP"})
    

def submitdata(email):
    from app import mysql
    cursor = mysql.connection.cursor()
    sql = "Update users set verifiedAt = (%s) where email = (%s)"
    val = (datetime.datetime.now(),email)
    cursor.execute(sql,val)
    mysql.connection.commit()
    cursor.close()

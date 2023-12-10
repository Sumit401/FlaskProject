from flask import Blueprint,jsonify, request
from .signup import OTP
verifyOTP_bp = Blueprint('verifyotp', __name__)

@verifyOTP_bp.route('/verifyotp', methods=["POST"])
def verifyotp():
    
    email = request.form["email"]
    otp = request.form["otp"]
    global OTP

    if(str(OTP[email]) == otp):
        return jsonify({"success" : True, "data" : "OTP verified scucessfully"})
    else:
        return jsonify({"success" : False,  "data" : "Incorrect OTP"})
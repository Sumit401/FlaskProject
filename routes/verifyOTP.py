from flask import Blueprint,jsonify, request,current_app
from .signup import OTP
import datetime
import jwt
from datetime import datetime, timedelta
from firebase_admin import firestore

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
    try:
        token = jwt.encode(payload={"data" : {"email" : email}, "exp" : (datetime.utcnow() + timedelta(minutes=10))},key=current_app.config['secretKey'],)
        user_ref = firestore.client().collection("users")
        document_ref = user_ref.document(email)
        document_snapshot = document_ref.get()
        if document_snapshot.exists:
            user_ref.document(email).update({"verifiedAt" : datetime.utcnow(), "token" : token})
        else:
            return False
    except Exception as e:
        return False
    return token
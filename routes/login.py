from datetime import datetime, timedelta

import jwt
from flask import Blueprint, current_app, jsonify, request
from firebase_admin import firestore

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    data = getData(email, password)
    return (data)

def getData(email,password):
    
    doc_ref = firestore.client().collection("users").document(email)
    doc_snapshot = doc_ref.get()
    if doc_snapshot.exists:
        document_data = doc_snapshot.to_dict()
        if document_data.get('password') == password: 
            if document_data.get("verifiedAt") == None:
                return jsonify({"success": True, "data" : "Login Sucessful but Email verification not done"}),203
            else:
                token = jwt.encode(payload={"data" : {
                    "email" : email,
                }, "exp" : (datetime.utcnow() + timedelta(minutes=10))},key=current_app.config['secretKey'],)
                doc_ref.update({"token" : token})
                return jsonify({"success": True, "data" : "Login SuccessFul", "token" : token}),200
        
    else:
        return jsonify({"success": False, "data" : "Invalid Credentials"}),400
    
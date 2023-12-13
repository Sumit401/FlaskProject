from datetime import datetime, timedelta

import jwt
from flask import Blueprint, current_app, jsonify, request
from firebase_admin import firestore

refreshToken_bp = Blueprint('refreshToken', __name__)

@refreshToken_bp.route('/refreshToken',  methods=['GET'])
def refreshToken():
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Invalid or missing token"}), 401  # 401 Unauthorized

    token = token.split(" ")[1]

    try:
        oldToken = jwt.decode(jwt=token,key= current_app.config['secretKey'],algorithms=['HS256'],options={"verify_signature": False},)

        if(firestore.client().collection("users").document(oldToken["data"]["email"]).get().to_dict().get("token") == token):
            refresh_Token = jwt.encode(payload={"data" :  oldToken["data"], "exp" : (datetime.utcnow() + timedelta(minutes=10))},key=current_app.config['secretKey'],)
        else:
            return jsonify({"success" : False,"data" : "unauthenticated"}),400
    except jwt.ExpiredSignatureError:
        return jsonify({"success" : False,"data" : "unauthenticated"}),400
    except jwt.InvalidTokenError:
        return jsonify({"success" : False,"data" : "unauthenticated"}),400

    return jsonify({"token":refresh_Token, "success" : True}),200

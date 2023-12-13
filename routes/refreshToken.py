from flask import Blueprint,jsonify,request,current_app
from datetime import datetime,timedelta
import jwt

refreshToken_bp = Blueprint('refreshToken', __name__)

@refreshToken_bp.route('/refreshToken')
def refreshToken():
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Invalid or missing token"}), 401  # 401 Unauthorized

    token = token.split(" ")[1]

    try:
        oldToken = jwt.decode(jwt=token,key= current_app.config['secretKey'],algorithms=['HS256'],options={"verify_signature": False},)
        refresh_Token = jwt.encode(payload={"data" :  oldToken["data"], "exp" : (datetime.utcnow() + timedelta(minutes=10))},key=current_app.config['secretKey'],)
    except jwt.ExpiredSignatureError:
        return "abcdx"
    except jwt.InvalidTokenError:
        return "abcdef"

    return jsonify({"token":refresh_Token, "success" : True})

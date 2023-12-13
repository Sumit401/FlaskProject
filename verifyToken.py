from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Invalid or missing token"}), 401  # 401 Unauthorized

        token = token.split(" ")[1]

        try:
            payload = jwt.decode(jwt=token,key= current_app.config['secretKey'],algorithms=['HS256'])
        except jwt.ExpiredSignatureError as e:
            print(f"Expired Token: {e}")
            return jsonify({"error": "Expired Token"}), 401  # 401 Unauthorized
        except jwt.InvalidTokenError as e:
            print(f"Invalid Token: {e}")
            return jsonify({"error": "Invalid Token","data":str(e)}), 401  # 401 Unauthorized

        return func(*args, payload=payload, **kwargs)

    return decorated

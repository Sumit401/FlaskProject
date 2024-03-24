from flask import Blueprint,jsonify

from verifyToken import token_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
@token_required
def home(payload):
    email = payload["data"]["email"]
    return jsonify()
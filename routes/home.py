from flask import Blueprint
from verifyToken import token_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['GET'])
@token_required
def home(payload):
    
    return payload

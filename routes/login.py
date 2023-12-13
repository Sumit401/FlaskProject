from flask import Blueprint, request,jsonify,current_app
import jwt
from datetime import datetime, timedelta

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    data = getData(email, password)
    return (data)

def getData(email,password):
    from app import mysql
    cursor = mysql.connection.cursor()
    sql = "Select * from users where email = (%s) AND password = (%s)"
    val = (email,password)
    cursor.execute(sql,val)
    data = cursor.fetchall()
    if not data:
        return jsonify({"success": False, "data" : "Invalid Credentials"}),400
    else:
        for all in data:
            if(str(all[6]) == "None"):
                return jsonify({"success":False, "data" : "Login Sucessful but OTP not verified"}), 401
            else:
                token = jwt.encode(payload={"data" : {
                    "email" : all[2],
                    "id" : all[0]
                }, "exp" : (datetime.utcnow() + timedelta(minutes=10))},key=current_app.config['secretKey'],)
                sql = "Update users set token = (%s) where email = (%s)"
                val = (token,email)
                cursor.execute(sql,val)
                mysql.connection.commit()
                return jsonify({"success" : True,"data" : "Login Sucessful OTP Verified","token": token, "value" : all[2]})
    cursor.close()
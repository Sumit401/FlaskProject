from flask import Blueprint, request,jsonify

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
    cursor.close()
    if not data:
        return jsonify({"success": False, "data" : "Invalid Credentials"}),400
    else:
        for all in data:
            if(str(all[6]) == "None"):
                return jsonify({"success":False, "data" : "Login Sucessfull but OTP not verified"}), 401
            else:
                return jsonify({"sucess" : True,"data" : "Login Sucessful OTP Verified"})

from flask import Blueprint, jsonify, current_app
from flask_mysqldb import MySQL

about_bp = Blueprint('about', __name__)

@about_bp.route('/about')
def about():
        # Access the MySQL extension object using current_app
        from app import mysql

        # Execute a SQL query to select all rows from the 'users' table
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")

        # Fetch the results and format as a list of dictionaries
        data = cursor.fetchall()

        # Close the cursor and the MySQL connection
        cursor.close()
        mapData = {
              "success" : False,
              "data" : []
        }
        
        if not data:
            mapData["error"] = "Empty list"
        else:
            for all in data:
                map = {
                    "id" : all[0],
                    "name" : all[1],
                    "email" : all[2],
                    "pass" : all[3],
                }
                mapData["success"] = True
                mapData["data"].append(map)
        
        # Return the data as JSON
        return jsonify(mapData)

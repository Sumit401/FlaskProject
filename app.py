from routes import create_app
from flask_mysqldb import MySQL

app = create_app()

# Initialize the MySQL extension
mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)
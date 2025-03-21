from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",  
    user="root",  
    password="",  
    database="practiceDB"  
)

@app.route('/')
def home():
    return "Flask is connected to MySQL!"

@app.route('/data', methods=['GET'])
def get_data():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spotifydatasetPractice LIMIT 10;")  # Change table name
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)  # Returns JSON response

if __name__ == '__main__':
    app.run(debug=True)
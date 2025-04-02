from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# MySQL Database Connection
conn = mysql.connector.connect(
    host="musicreview.c1comakqsr9e.us-east-2.rds.amazonaws.com",  
    user="GregElDeiry",  
    password="COP4710gce22",  
    database="musicreview"  
)

@app.route('/')
def home():
    return "Flask is connected to MySQL!"

@app.route('/Songs', methods=['GET'])
def get_songs():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Songs LIMIT 200;")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/Artists', methods=['GET'])
def get_artists():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Artists LIMIT 200;")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/Albums', methods=['GET'])
def get_albums():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Albums LIMIT 200;")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/data', methods=['GET'])
def get_data():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM song LIMIT 200;")  # Change table name
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)  # Returns JSON response

if __name__ == '__main__':
    app.run(debug=True)
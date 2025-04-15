# from flask import Flask, jsonify
# from flask import request
# from flask_cors import CORS
# import mysql.connector
# from mysql.connector import Error


# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend access



# # MySQL Database Connection
# conn = mysql.connector.connect(
#     host="musicreview.c1comakqsr9e.us-east-2.rds.amazonaws.com",  
#     user="GregElDeiry",  
#     password="COP4710gce22",  
#     database="musicreview"  
# ) 




# @app.route('/api/songs', methods=['GET'])
# def search_songs():
#     try:
#         query = request.args.get('search', '')
#         cursor = conn.cursor(dictionary=True)
#         like_query = f"%{query}%"
#         sql = """
#             SELECT 
#                 Songs.Title as song_title, 
#                 Songs.Spotify_ID as spotify_id,
#                 Artists.Artist_Name as artist_name,
#                 Albums.Album_Name as album_name
#             FROM Songs
#             JOIN Artists ON Songs.Artist_ID = Artists.Artist_ID
#             JOIN Albums ON Songs.Album_ID = Albums.Album_ID
#             WHERE Songs.Title LIKE %s 
#             OR Artists.Artist_Name LIKE %s
#             OR Albums.Album_Name LIKE %s
#             LIMIT 100
#         """  
        
#         cursor.execute(sql, (like_query, like_query, like_query)) 
#         results = cursor.fetchall() 
#         cursor.close() 
#         return jsonify(results)
#     except Exception as e:
#         print("Error in /api/songs route:", e)
#         return jsonify({"error": str(e)}), 500
# @app.route('/api/artists', methods=['GET'])
# def search_artists():
#     try: 
#         query = request.args.get('search', '')
#         cursor = conn.cursor(dictionary=True)
#         like_query = f"%{query}%"
#         sql = """
#             SELECT DISTINCT Artist_Name AS artist_name
#             FROM Artists
#             WHERE Artist_Name LIKE %s
#             LIMIT 100
#             """
#         cursor.execute(sql, (like_query,))
#         results = cursor.fetchall()
#         cursor.close()
#         return jsonify(results)
#     except Exception as e:
#         print ("Error in /api/artists route:", e)
#         return jsonify({"error": str(e)}), 500
# @app.route('/api/albums', methods=['GET'])
# def search_albums():
#     try:
#         query = request.args.get('search', '')
#         cursor = conn.cursor(dictionary=True)
#         like_query = f"%{query}%"
#         sql = """
#             SELECT DISTINCT Albums.Album_Name AS album_name
#             FROM Albums
#             WHERE Albums.Album_Name LIKE %s 
#             LIMIT 100;

#             """
#         cursor.execute(sql, (like_query, ))
#         results = cursor.fetchall()
#         cursor.close()
#         return jsonify(results)
#     except Exception as e:
#         print("Error in /api/albums route:", e)
#         return jsonify({"error": str(e)}), 500
    


# @app.route('/')
# def home():
#     return "Flask is connected to MySQL!"

# @app.route('/Songs', methods=['GET'])
# def get_songs():
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM Songs LIMIT 200;")
#     data = cursor.fetchall()
#     cursor.close()
#     return jsonify(data)

# @app.route('/Artists', methods=['GET'])
# def get_artists():
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM Artists LIMIT 200;")
#     data = cursor.fetchall()
#     cursor.close()
#     return jsonify(data)

# @app.route('/Albums', methods=['GET'])
# def get_albums():
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM Albums LIMIT 200;")
#     data = cursor.fetchall()
#     cursor.close()
#     return jsonify(data)

# @app.route('/data', methods=['GET'])
# def get_data():
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM song LIMIT 200;")  # Change table name
#     data = cursor.fetchall()
#     cursor.close()
#     return jsonify(data)  # Returns JSON response




# @app.route('/login', methods = ['POST'])
# def login_request():
#     try:
#        data = request.get_json()
#        username = data.get('username')
#        password = data.get('password')

#        cursor = conn.cursor(dictionary = True)
#        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#        user = cursor.fetchone()
#        cursor.close()

#        if user and user['password'] == password:
#            return jsonify({"success": True, "message": "Login Successful"})
#        else:
#            return jsonify({"success": False, "message": "Invalid Credentials"}), 401
       
#     except Exception as e:
#        return jsonify({"success": False, "message": str(e)}), 500
       

# @app.route('/api/submit_review', methods=['POST'])
# def submit_song_review():
#     try:
#         # Get the review data from the request
#         data = request.get_json()
        
#         # Extract review details
#         username = data.get('username')
#         song_id = data.get('song_id')
#         rating = data.get('rating')
#         review_text = data.get('review_text')
        
#         # Validate input
#         if not all([username, song_id, rating, review_text]):
#             return jsonify({"success": False, "message": "Missing required review details"}), 400
        
#         # Validate rating is an integer between 1 and 5
#         try:
#             rating = int(rating)
#             if rating < 1 or rating > 5:
#                 return jsonify({"success": False, "message": "Rating must be between 1 and 5"}), 400
#         except ValueError:
#             return jsonify({"success": False, "message": "Invalid rating"}), 400
        
#         # Create a cursor
#         cursor = conn.cursor(dictionary=True)
        
#         # Check if user exists
#         cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#         user = cursor.fetchone()
#         if not user:
#             cursor.close()
#             return jsonify({"success": False, "message": "User not found"}), 404
        
#         # Check if song exists
#         cursor.execute("SELECT * FROM Songs WHERE Spotify_ID = %s", (song_id,))
#         song = cursor.fetchone()
#         if not song:
#             cursor.close()
#             return jsonify({"success": False, "message": "Song not found"}), 404
        
#         # Insert the review
#         insert_query = """
#         INSERT INTO Song_Reviews 
#         (reviewer_username, song_ID, rating, review, created_at) 
#         VALUES (%s, %s, %s, %s, NOW())
#         """
#         cursor.execute(insert_query, (username, song_id, rating, review_text))
        
#         # Commit the transaction
#         conn.commit()
        
#         # Close the cursor
#         cursor.close()
        
#         return jsonify({"success": True, "message": "Review submitted successfully"}), 201
    
#     except mysql.connector.Error as err:
#         # Rollback in case of any database error
#         conn.rollback()
#         print(f"Database error: {err}")
#         return jsonify({"success": False, "message": "Database error occurred"}), 500
    
#     except Exception as e:
#         # Catch any other unexpected errors
#         print(f"Unexpected error: {e}")
#         return jsonify({"success": False, "message": "An unexpected error occurred"}), 500

# @app.route('/api/song/<song_id>', methods=['GET'])
# def get_song_details(song_id):
#     try:
#         cursor = conn.cursor(dictionary=True)
#         sql = """
#             SELECT 
#                 Songs.Spotify_ID, 
#                 Songs.Title, 
#                 Artists.Artist_Name, 
#                 Albums.Album_Name
#             FROM Songs
#             JOIN Artists ON Songs.Artist_ID = Artists.Artist_ID
#             JOIN Albums ON Songs.Album_ID = Albums.Album_ID
#             WHERE Songs.Spotify_ID = %s
#         """
#         cursor.execute(sql, (song_id,))
#         song = cursor.fetchone()
#         cursor.close()

#         if song:
#             return jsonify(song)
#         else:
#             return jsonify({"error": "Song not found"}), 404
#     except Exception as e:
#         print(f"Error fetching song details: {e}")
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/song_reviews/<song_id>', methods=['GET'])
# def get_song_reviews(song_id):
#     try:
#         cursor = conn.cursor(dictionary=True)
#         sql = """
#             SELECT 
#                 reviewer_username, 
#                 rating, 
#                 review, 
#                 created_at
#             FROM Song_Reviews
#             WHERE song_ID = %s
#             ORDER BY created_at DESC
#         """
#         cursor.execute(sql, (song_id,))
#         reviews = cursor.fetchall()
#         cursor.close()

#         return jsonify(reviews)
#     except Exception as e:
#         print(f"Error fetching song reviews: {e}")
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Database configuration
db_config = {
    "host": "musicreview.c1comakqsr9e.us-east-2.rds.amazonaws.com",  
    "user": "GregElDeiry",  
    "password": "COP4710gce22",  
    "database": "musicreview"
}

# Function to get a fresh database connection
def get_db_connection():
    try:
        print("Creating new database connection...")
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Function to ensure we have a working connection
def ensure_connection():
    connection = get_db_connection()
    if connection and connection.is_connected():
        return connection
    else:
        print("Failed to establish database connection")
        return None

@app.route('/api/songs', methods=['GET'])
def search_songs():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        query = request.args.get('search', '')
        cursor = connection.cursor(dictionary=True)
        like_query = f"%{query}%"
        sql = """
            SELECT 
                Songs.Title as song_title, 
                Songs.Spotify_ID as spotify_id,
                Artists.Artist_Name as artist_name,
                Albums.Album_Name as album_name
            FROM Songs
            JOIN Artists ON Songs.Artist_ID = Artists.Artist_ID
            JOIN Albums ON Songs.Album_ID = Albums.Album_ID
            WHERE Songs.Title LIKE %s 
            OR Artists.Artist_Name LIKE %s
            OR Albums.Album_Name LIKE %s
            LIMIT 100
        """  
        
        cursor.execute(sql, (like_query, like_query, like_query)) 
        results = cursor.fetchall() 
        cursor.close() 
        connection.close()
        return jsonify(results)
    except Exception as e:
        print("Error in /api/songs route:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/artists', methods=['GET'])
def search_artists():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        query = request.args.get('search', '')
        cursor = connection.cursor(dictionary=True)
        like_query = f"%{query}%"
        sql = """
            SELECT DISTINCT Artist_Name AS artist_name
            FROM Artists
            WHERE Artist_Name LIKE %s
            LIMIT 100
            """
        cursor.execute(sql, (like_query,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(results)
    except Exception as e:
        print("Error in /api/artists route:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/albums', methods=['GET'])
def search_albums():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        query = request.args.get('search', '')
        cursor = connection.cursor(dictionary=True)
        like_query = f"%{query}%"
        sql = """
            SELECT DISTINCT Albums.Album_Name AS album_name
            FROM Albums
            WHERE Albums.Album_Name LIKE %s 
            LIMIT 100;
            """
        cursor.execute(sql, (like_query, ))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(results)
    except Exception as e:
        print("Error in /api/albums route:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def home():
    return "Flask is connected to MySQL!"

@app.route('/Songs', methods=['GET'])
def get_songs():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Songs LIMIT 200;")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        print("Error in /Songs route:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/Artists', methods=['GET'])
def get_artists():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Artists LIMIT 200;")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        print("Error in /Artists route:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/Albums', methods=['GET'])
def get_albums():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Albums LIMIT 200;")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        print("Error in /Albums route:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM song LIMIT 200;")  # Change table name
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(data)
    except Exception as e:
        print("Error in /data route:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login_request():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and user['password'] == password:
            return jsonify({"success": True, "message": "Login Successful"})
        else:
            return jsonify({"success": False, "message": "Invalid Credentials"}), 401
    except Exception as e:
        print("Error in /login route:", e)
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/submit_review', methods=['POST'])
def submit_song_review():
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        # Get the review data from the request
        data = request.get_json()
        
        # Extract review details
        username = data.get('username')
        song_id = data.get('song_id')
        rating = data.get('rating')
        review_text = data.get('review_text')
        
        # Validate input
        if not all([username, song_id, rating, review_text]):
            return jsonify({"success": False, "message": "Missing required review details"}), 400
        
        # Validate rating is an integer between 1 and 5
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({"success": False, "message": "Rating must be between 1 and 5"}), 400
        except ValueError:
            return jsonify({"success": False, "message": "Invalid rating"}), 400
        
        # Create a cursor
        cursor = connection.cursor(dictionary=True)
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            connection.close()
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Check if song exists
        cursor.execute("SELECT * FROM Songs WHERE Spotify_ID = %s", (song_id,))
        song = cursor.fetchone()
        if not song:
            cursor.close()
            connection.close()
            return jsonify({"success": False, "message": "Song not found"}), 404
        
        # Insert the review
        insert_query = """
        INSERT INTO Song_Reviews 
        (reviewer_username, song_ID, rating, review, created_at) 
        VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (username, song_id, rating, review_text))
        
        # Commit the transaction
        connection.commit()
        
        # Close the cursor
        cursor.close()
        connection.close()
        
        return jsonify({"success": True, "message": "Review submitted successfully"}), 201
    
    except mysql.connector.Error as err:
        # Rollback in case of any database error
        if 'connection' in locals() and connection:
            connection.rollback()
            connection.close()
        print(f"Database error: {err}")
        return jsonify({"success": False, "message": "Database error occurred"}), 500
    
    except Exception as e:
        # Catch any other unexpected errors
        if 'connection' in locals() and connection:
            connection.close()
        print(f"Unexpected error: {e}")
        return jsonify({"success": False, "message": "An unexpected error occurred"}), 500

@app.route('/api/song/<song_id>', methods=['GET'])
def get_song_details(song_id):
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        print(f"Looking up song details for ID: {song_id}")
        cursor = connection.cursor(dictionary=True)
        sql = """
            SELECT 
                Songs.Spotify_ID, 
                Songs.Title, 
                Artists.Artist_Name, 
                Albums.Album_Name
            FROM Songs
            JOIN Artists ON Songs.Artist_ID = Artists.Artist_ID
            JOIN Albums ON Songs.Album_ID = Albums.Album_ID
            WHERE Songs.Spotify_ID = %s
        """
        cursor.execute(sql, (song_id,))
        song = cursor.fetchone()
        cursor.close()
        connection.close()

        if song:
            print(f"Found song details: {song}")
            return jsonify(song)
        else:
            print(f"Song not found with ID: {song_id}")
            return jsonify({"error": "Song not found"}), 404
    except Exception as e:
        import traceback
        print(f"Error fetching song details: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/song_reviews/<song_id>', methods=['GET'])
def get_song_reviews(song_id):
    try:
        # Get a fresh connection for this request
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        print(f"Looking up reviews for song ID: {song_id}")
        cursor = connection.cursor(dictionary=True)
        sql = """
            SELECT 
                reviewer_username, 
                rating, 
                review, 
                created_at
            FROM Song_Reviews
            WHERE song_ID = %s
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (song_id,))
        reviews = cursor.fetchall()
        cursor.close()
        connection.close()

        print(f"Found {len(reviews)} reviews for song ID: {song_id}")
        return jsonify(reviews)
    except Exception as e:
        import traceback
        print(f"Error fetching song reviews: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    try:
        connection = ensure_connection()
        if not connection:
            return jsonify({"status": "error", "message": "Could not establish database connection"}), 500
            
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as connection_test")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return jsonify({
            "status": "success", 
            "message": "Database connection working", 
            "result": result
        })
    except Exception as e:
        import traceback
        print(f"Error testing connection: {e}")
        print(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

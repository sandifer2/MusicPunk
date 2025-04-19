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
        
        # Check if user has already reviewed this song
        cursor.execute("SELECT * FROM Song_Reviews WHERE reviewer_username = %s AND song_id = %s", (username, song_id))
        existing_review = cursor.fetchone()
        if existing_review:
            cursor.close()
            connection.close() 
            return jsonify({"success": False, "message": "You've already reviewed this song"}), 409
        
        try:
            # Insert the review
            insert_query = """
            INSERT INTO Song_Reviews 
            (reviewer_username, song_ID, rating, review, created_at) 
            VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(insert_query, (username, song_id, rating, review_text))
            
            # Add 10 tokens to the user's balance
            cursor.execute("""
                UPDATE users 
                SET tokens = tokens + 10 
                WHERE username = %s
            """, (username,))
            
            # Get the updated token count
            cursor.execute("SELECT tokens FROM users WHERE username = %s", (username,))
            updated_user = cursor.fetchone()
            
            # Commit the transaction
            connection.commit()
            
            # Close the cursor
            cursor.close()
            connection.close()
            
            return jsonify({
                "success": True, 
                "message": "Review submitted successfully",
                "tokens_earned": 10,
                "new_token_balance": updated_user['tokens']
            }), 201
            
        except Exception as e:
            connection.rollback()
            raise e
            
    except Exception as e:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        print(f"Error submitting review: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

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
@app.route('/api/user/tokens', methods=['GET'])
def get_user_tokens():
    try:
        # Get a fresh connection
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        # Get username from session or request
        username = request.args.get('username')
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT tokens FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            return jsonify({"tokenCount": result['tokens']})
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        print(f"Error fetching user tokens: {e}")
        return jsonify({"error": str(e)}), 500 
@app.route('/api/check_song_unlock/<song_id>', methods=['GET'])
def check_song_unlock(song_id):
    try:
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        username = request.args.get('username')
        if not username:
            return jsonify({"error": "Username is required"}), 400

        cursor = connection.cursor(dictionary=True)
        
        # Check if song is unlocked for this user
        cursor.execute("""
            SELECT * FROM Unlocked_Songs 
            WHERE username = %s AND song_id = %s
        """, (username, song_id))
        
        is_unlocked = cursor.fetchone() is not None
        
        # Get user's token count
        cursor.execute("SELECT tokens FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            "is_unlocked": is_unlocked,
            "tokens_available": user['tokens'] if user else 0,
            "unlock_cost": 5  # Fixed cost to unlock a song
        })
        
    except Exception as e:
        print(f"Error checking song unlock status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/unlock_song', methods=['POST'])
def unlock_song():
    try:
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        data = request.get_json()
        username = data.get('username')
        song_id = data.get('song_id')
        token_cost = 5  # Cost to unlock a song
        
        if not all([username, song_id]):
            return jsonify({"error": "Missing username or song_id"}), 400

        cursor = connection.cursor(dictionary=True)
        
        # Check if song is already unlocked
        cursor.execute("""
            SELECT * FROM Unlocked_Songs 
            WHERE username = %s AND song_id = %s
        """, (username, song_id))
        
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({"error": "Song is already unlocked"}), 409

        # Check if user has enough tokens
        cursor.execute("SELECT tokens FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            connection.close()
            return jsonify({"error": "User not found"}), 404
            
        if user['tokens'] < token_cost:
            cursor.close()
            connection.close()
            return jsonify({
                "error": "Insufficient tokens",
                "tokens_available": user['tokens'],
                "tokens_needed": token_cost
            }), 400

        try:
            # Deduct tokens from user
            cursor.execute("""
                UPDATE users 
                SET tokens = tokens - %s 
                WHERE username = %s
            """, (token_cost, username))
            
            # Add record to Unlocked_Songs
            cursor.execute("""
                INSERT INTO Unlocked_Songs (username, song_id, unlocked_at)
                VALUES (%s, %s, NOW())
            """, (username, song_id))
            
            # Commit the changes
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return jsonify({
                "success": True,
                "message": "Song unlocked successfully",
                "tokens_remaining": user['tokens'] - token_cost
            })
            
        except Exception as e:
            # Rollback in case of error
            connection.rollback()
            cursor.close()
            connection.close()
            raise e
            
    except Exception as e:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        print(f"Error unlocking song: {e}")
        return jsonify({"error": str(e)}), 500
    

# endpoint to get all reviews for a user
@app.route('/api/user/reviews', methods=['GET'])
def get_user_reviews():
    try:
        # Get a fresh connection
        connection = ensure_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
            
        # Get username from query parameters
        username = request.args.get('username')
        if not username:
            return jsonify({"error": "Username is required"}), 400
        
        cursor = connection.cursor(dictionary=True)
        
        # Query to get all reviews by the user with song details
        sql = """
            SELECT 
                sr.song_review_ID AS review_id,
                sr.song_ID AS song_id,
                s.Title AS song_title,
                a.Artist_Name AS artist_name,
                al.Album_Name AS album_name,
                sr.rating,
                sr.review,
                sr.created_at
            FROM Song_Reviews sr
            JOIN Songs s ON sr.song_ID = s.Spotify_ID
            JOIN Artists a ON s.Artist_ID = a.Artist_ID
            JOIN Albums al ON s.Album_ID = al.Album_ID
            WHERE sr.reviewer_username = %s
            ORDER BY sr.created_at DESC
        """
        
        cursor.execute(sql, (username,))
        reviews = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify(reviews)
        
    except Exception as e:
        print(f"Error fetching user reviews: {e}")
        return jsonify({"error": str(e)}), 500
   









if __name__ == '__main__':
    app.run(debug=True)

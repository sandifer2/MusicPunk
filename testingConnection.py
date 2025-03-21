import mysql.connector

# Establish connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="practiceDB"
)

if conn.is_connected():
    print("Connected to MySQL database successfully!")

    # Create a cursor object to execute queries
    cursor = conn.cursor()

    # Example 1: Show all tables
    cursor.execute("SELECT * FROM spotifydatasetPractice LIMIT 10;")
    print("Tables in the database:")
    for table in cursor:
        print(table)

    # # Example 2: Insert data (Modify as per your table structure)
    # try:
    #     cursor.execute("INSERT INTO your_table (column1, column2) VALUES ('value1', 'value2');")
    #     conn.commit()  # Save the changes
    #     print("Data inserted successfully!")
    # except mysql.connector.Error as err:
    #     print(f"Error: {err}")

    # # Example 3: Retrieve data
    # cursor.execute("SELECT * FROM your_table;")
    # print("Data in your_table:")
    # for row in cursor.fetchall():
    #     print(row)

    # Close the cursor
    cursor.close()

# Close connection
conn.close()
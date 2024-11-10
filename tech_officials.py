from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': "test"
}
def get_db_connection():
    return mysql.connector.connect(**db_config)
@app.route('/')
def home():
    # Connect to the database and retrieve tech_officials data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tech_of")
    tech_officials = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Render the tech_officials page with the fetched data
    return render_template('tech_officials.html', tech_officials=tech_officials)

if __name__ == '__main__':
    app.run(debug=True)
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

# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/coaches')
def cocahes():
    # Connect to the database and retrieve coaches data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM coaches")
    coaches = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Render the coaches page with the fetched data
    return render_template('coaches.html', coaches=coaches)

@app.route("/medal")
def medal_page():
    conn = get_db_connection()




    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medal")  # Ensure that the table name is correct
    medals = cursor.fetchall()


        
    cursor.close()


    
    conn.close()


    return render_template("medals.html", medals=medals)

@app.route('/tech')
def techpage():
    # Connect to the database and retrieve tech_officials data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tech_officials")
    tech_officials = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Render the tech_officials page with the fetched data
    return render_template('tech_officials.html', tech_officials=tech_officials)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import mysql.connector
from flask import request

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    'database': "test"
}

# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(**db_config)



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')



@app.route('/coaches')
def coaches():
    # Connect to the database and retrieve coaches data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM coaches")
    coaches = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Render the coaches page with the fetched data
    return render_template('coaches.html', coaches=coaches)

@app.route('/country', methods=['GET'])
def country():
    
    country = request.args.get('country')
    # Connect to the database and retrieve coaches data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if country:
        cursor.execute("SELECT * FROM country WHERE country_code = %s", (country,))
    else:
        cursor.execute("SELECT * FROM country")
    countries = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Render the coaches page with the fetched data
    return render_template('country.html', countries=countries)

@app.route("/medal")
def medal():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medal ORDER BY athlete_short_name")  # Ensure that the table name is correct
    medals = cursor.fetchall() 
    cursor.close()
    conn.close()


    return render_template("medals.html", medals=medals)

@app.route('/tech')
def tech():
    # Connect to the database and retrieve tech_officials data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tech_of")
    tech_officials = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Render the tech_officials page with the fetched data
    return render_template('tech_officials.html', tech_officials=tech_officials)

@app.route('/athletes', methods=['GET'])
def athletes():
    
    athletes = request.args.get('athletes')
    # Connect to the database and retrieve coaches data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if athletes:
        cursor.execute("SELECT * FROM athletes WHERE name = %s", (athletes,))
    else:
        cursor.execute("SELECT * FROM athletes")
    athleties = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Render the coaches page with the fetched data
    return render_template('athletes.html', athletes=athleties)

if __name__ == '__main__':
    app.run(debug=True)



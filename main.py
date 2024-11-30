from flask import Flask, render_template, redirect, url_for
import mysql.connector
from flask import request

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',
    'password': 'Qweasdqwe123.',
    'host': 'localhost',
    'database': "database_final"
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

@app.route('/delete_coaches>', methods=['POST'])
def delete_coaches():
    Coach_name = request.args.get('coaches')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coaches WHERE Coach_name = %s", (Coach_name,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('coaches'))

@app.route('/insert_coach', methods=['POST'])
def insert_coach():
    # Retrieve form data
    name = request.form.get('name')
    gender = request.form.get('gender')
    birth_date = request.form.get('birth_date')
    country_code = request.form.get('country_code')
    discipline = request.form.get('discipline')
    function = request.form.get('function')

    # Insert the new coach into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO coaches (Coach_name, Gender, Birth_date, Country_code, Discipline, coaches.Function)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, gender, birth_date, country_code, discipline, function))
    conn.commit()
    cursor.close()
    conn.close()

    # Redirect back to the coaches page
    return "<script>alert('Coach added successfully!'); window.location.href='/coaches';</script>"

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

@app.route('/delete_country>', methods=['POST'])
def delete_country():
    country = request.args.get('country')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM country WHERE Country_code = %s", (country,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('country')) # No content response


@app.route("/medal")
def medal():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medal ORDER BY Athlete_short_name")  # Ensure that the table name is correct
    medals = cursor.fetchall() 
    cursor.close()
    conn.close()


    return render_template("medals.html", medals=medals)

@app.route('/delete_medal>', methods=['POST'])
def delete_medal():
    medal_id = request.args.get('medal')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medal WHERE Medal_id = %s", (medal_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('medal')) # No content response


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


@app.route('/delete_tech>', methods=['POST'])
def delete_tech():
    tech_id = request.args.get('tech')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tech_of WHERE Tech_id = %s", (tech_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('tech')) # No content response

@app.route('/insert_tech', methods=['POST'])
def insert_tech():
    # Retrieve form data
    tech_name = request.form.get('tech_name')
    gender = request.form.get('gender')
    birth_date = request.form.get('birth_date')
    country = request.form.get('country')
    country_code = request.form.get('country_code')
    discipline = request.form.get('discipline')
    function = request.form.get('function')

    # Insert the new tech official into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO tech_of (Tech_name, Gender, Birth_date, Country, Country_code, Discipline, tech_of.Function)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (tech_name, gender, birth_date, country, country_code, discipline, function))
    conn.commit()
    cursor.close()
    conn.close()

    # Redirect back to the technical officials page
    return "<script>alert('Technical Official added successfully!'); window.location.href='/tech';</script>"



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

@app.route('/delete_athlete>', methods=['POST'])
def delete_athlete():
    Athlete_name = request.args.get('athletes')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM athletes WHERE Athlete_name = %s", (Athlete_name,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('athletes')) # No content response


@app.route('/discipline', methods=['GET'])
def discipline():
    discipline_name = request.args.get('discipline')
    # Connect to the database and retrieve disciplines data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if discipline_name:
        cursor.execute("SELECT * FROM discipline WHERE Discipline = %s", (discipline_name,))
    else:
        cursor.execute("SELECT * FROM discipline")
    disciplines = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('discipline.html', disciplines=disciplines)

@app.route('/delete_discipline>', methods=['POST'])
def delete_discipline():
    Discipline = request.args.get('discipline')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM discipline WHERE Discipline = %s", (Discipline,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('discipline')) # No content response


@app.route('/events', methods=['GET'])
def events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events_")  # Ensure table name matches
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('events.html', events=events)

@app.route('/delete_event>', methods=['POST'])
def delete_event():
    stage = request.args.get('events')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events_ WHERE Event_stage = %s", (stage,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('events'))

@app.route('/insert_event', methods=['POST'])
def insert_event():
    # Retrieve form data
    event_stage = request.form.get('event_stage')
    location = request.form.get('location')
    event_status = request.form.get('event_status')
    time = request.form.get('time')
    discipline = request.form.get('discipline')

    # Insert the new event into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO events_ (Event_stage, Location, Event_status, Time, Discipline)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (event_stage, location, event_status, time, discipline))
    conn.commit()
    cursor.close()
    conn.close()

    # Redirect back to the events page
    return "<script>alert('Event added successfully!'); window.location.href='/events';</script>"

if __name__ == '__main__':
    app.run(debug=True)



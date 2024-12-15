from flask import Flask, render_template, redirect, url_for
import mysql.connector
from flask import request
import math

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',
    'password': 'Qweasdqwe123.',
    'host': 'localhost',
    'database': "database"
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
    Coach_id = request.args.get('coaches')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coaches WHERE Coach_id = %s", (Coach_id,))
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
    discipline_id = request.form.get('discipline_id')
    function = request.form.get('function')

    # Insert the new coach into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO coaches (Coach_name, Gender, Birth_date, Country_code, Discipline_id, coaches.Function)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, gender, birth_date, country_code, discipline_id, function))

    conn.commit()
    cursor.close()
    conn.close()

    # Redirect back to the coaches page
    return "<script>alert('Coach added successfully!'); window.location.href='/coaches';</script>"

@app.route('/update_coach', methods=['POST'])
def update_coach():
    # Retrieve form data
    coach_id = request.form.get('coach_id')  
    name = request.form.get('name')
    gender = request.form.get('gender')
    birth_date = request.form.get('birth_date')
    country_code = request.form.get('country_code')
    discipline = request.form.get('discipline')  
    function = request.form.get('function')

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()


    query = """
    UPDATE coaches
    SET Coach_name = COALESCE(%s, Coach_name),
        Gender = COALESCE(%s, Gender),
        Birth_date = COALESCE(%s, Birth_date),
        Country_code = COALESCE(%s, Country_code),
        Discipline = COALESCE(%s, Discipline),
        `Function` = COALESCE(%s, `Function`)
    WHERE Coach_id = %s
    """
    
    # Execute the first query to update the coach's information
    cursor.execute(query, (name, gender, birth_date, country_code, discipline, function, coach_id))

    # Now use the same `discipline` from the form to update the `Discipline_id`

    # Commit the changes
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect back to the coaches page with a success message
    return "<script>alert('Coach updated successfully!'); window.location.href='/coaches';</script>"

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

@app.route('/insert_country', methods=['POST'])
def insert_country():
    # Retrieve form data
    country_code = request.form.get('country_code')
    gold = int(request.form.get('gold'))
    silver = int(request.form.get('silver'))
    bronze = int(request.form.get('bronze'))
    rank = int(request.form.get('rank'))
    total = gold + silver + bronze
    
    
    total = gold + silver + bronze

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

        # Insert data into the database
    query = """
    INSERT INTO country (Country_code, Gold, Silver, Bronze, Total, country.Rank)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (country_code, gold, silver, bronze, total, rank))
    conn.commit()

        # Close the database connection
    cursor.close()
    conn.close()

        # Redirect back to the countries page
    return "<script>alert('Country added successfully!'); window.location.href='/country';</script>"

@app.route('/update_country', methods=['POST'])
def update_country():
    # Retrieve form data
    country_code = request.form.get('country_code')
    gold = int(request.form.get('gold'))
    silver = int(request.form.get('silver'))
    bronze = int(request.form.get('bronze'))
    rank = int(request.form.get('rank'))
    total = gold + silver + bronze

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE country
    SET Gold = %s,
        Silver = %s,
        Bronze = %s,
        `Rank` = %s,
        Total = %s
    WHERE Country_code = %s
    """

    cursor.execute(query, (gold, silver, bronze, rank, total, country_code))

    # Commit the changes
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return "<script>alert('Country updated successfully!'); window.location.href='/country';</script>"

@app.route('/medal')
def medal():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch medal data along with athlete names
    cursor.execute("""
        SELECT m.*, a.Athlete_name AS Athlete_name
        FROM medal m
        JOIN athletes a ON m.Athlete_id = a.Athlete_id
        ORDER BY a.Athlete_name ASC;
    """)
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

@app.route('/insert_medal', methods=['POST'])
def insert_medal():
    # Retrieve form data
    Medal_type = request.form.get('medal_type')
    Medal_code = request.form.get('medal_code')
    Athlete_sex = request.form.get('athlete_sex')
    Event_id = request.form.get('event_id')
    Country_code = request.form.get('country_code')
    Medal_date = request.form.get('medal_date')

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert data into the database
    query = """
    INSERT INTO medal (Medal_type, Medal_code, Athlete_sex, Event_id, Country_code)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (Medal_type, Medal_code, Athlete_sex, Event_id, Medal_date, Country_code))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect back to the medals page with a success message
    return "<script>alert('Medal added successfully!'); window.location.href='/medal';</script>"

@app.route('/update_medal', methods=['POST'])
def update_medal():
    # Retrieve form data
    Medal_id = request.args.get('medal')  # Assuming the medal ID is passed as a query parameter
    Medal_type = request.form.get('medal_type')
    Medal_code = request.form.get('medal_code')
    Athlete_sex = request.form.get('athlete_sex')
    Event_id = request.form.get('event_id')
    Country_code = request.form.get('country_code')
    Medal_date = request.form.get('medal_date')

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Corrected UPDATE query with WHERE clause
    query = """
    UPDATE medal 
    SET Medal_type = COALESCE(%s, Medal_type), 
    Medal_code = COALESCE(%s, Medal_code),
    Medal_date = COALESCE(%s, Medal_date), 
    Athlete_sex = COALESCE(%s, Athlete_sex), 
    Event_id = COALESCE(%s, Event_id), 
    Country_code = COALESCE(%s, Country_code)
    WHERE Medal_id = %s
    """

    cursor.execute(query, (Medal_type, Medal_code,Medal_date, Athlete_sex, Event_id, Country_code, Medal_id))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect back to the medals page with a success message
    return "<script>alert('Medal updated successfully!'); window.location.href='/medal';</script>"


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
    country_code = request.form.get('country_code')
    discipline_id = request.form.get('discipline_id')
    function = request.form.get('function')

    # Insert the new tech official into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO tech_of (Tech_name, Gender, Birth_date, Country_code, Discipline_id, tech_of.Function)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (tech_name, gender, birth_date, country_code, discipline_id, function))

    conn.commit()
    cursor.close()
    conn.close()

    # Redirect back to the technical officials page
    return "<script>alert('Technical Official added successfully!'); window.location.href='/tech';</script>"

@app.route('/update_tech', methods=['POST'])
def update_tech():
    # Retrieve form data
    tech_id = request.form.get('tech_id')
    tech_name = request.form.get('tech_name')
    gender = request.form.get('gender')
    birth_date = request.form.get('birth_date')
    country_code = request.form.get('country_code')
    discipline_id = request.form.get('discipline_id')
    function = request.form.get('function')

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE tech_of
    SET Tech_name = %s,
        Gender = %s,
        Birth_date = %s,
        Country_code = %s,
        Discipline_id = %s,
        `Function` = %s
    WHERE Tech_id = %s
    """

    cursor.execute(query, (tech_name, gender, birth_date, country_code, discipline_id, function, tech_id))

    # Commit the changes
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return "<script>alert('Technical Official updated successfully!'); window.location.href='/tech';</script>"

@app.route('/athletes', methods=['GET'])
def athletes():
    # Get the current page number from the URL, default to page 1
    page = request.args.get('page', 1, type=int)
    
    # Set the number of athletes per page
    per_page = 50
    
    # Calculate the offset for the query
    offset = (page - 1) * per_page
    
    # Connect to the database and retrieve athletes data with pagination
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    Athlete_id = request.args.get('athletes')
    Country_code = request.args.get('country_code')
    cursor.execute("SELECT COUNT(*) FROM athletes")
    total_athletes = cursor.fetchone()['COUNT(*)']
    total_pages = math.ceil(total_athletes / per_page)
    # Fetch the total count of athletes to calculate total pages
    if Athlete_id:
        cursor.execute("SELECT * FROM athletes WHERE Athlete_id = %s", (Athlete_id,))
    if Country_code:
        cursor.execute("SELECT * FROM athletes WHERE Country_code = %s", (Country_code,))
    else:
        
    
        # Fetch athletes for the current page
        cursor.execute("SELECT * FROM athletes LIMIT %s OFFSET %s", (per_page, offset))
    
    
    athletes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Calculate the total number of pages
    
    
    # Render the athletes page with the current page and total pages
    return render_template('athletes.html', athletes=athletes, page=page, total_pages=total_pages)

@app.route('/delete_athlete>', methods=['POST'])
def delete_athlete():
    Athlete_id = request.args.get('athletes')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM athletes WHERE Athlete_id = %s", (Athlete_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('athletes')) # No content response

@app.route('/insert_athlete', methods=['POST'])
def insert_athlete():
    # Retrieve form data
    Athlete_name = request.form.get('athlete_name')
    Short_name = request.form.get('short_name')
    Gender = request.form.get('gender')
    Birth_place = request.form.get('birth_place')
    Birth_country = request.form.get('birth_country')
    Country_code = request.form.get('country_code')
    Discipline_id = request.form.get('discipline_id')


    

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

        # Insert data into the database
    query = """
    INSERT INTO athletes (Athlete_name, Short_name, Gender, Birth_place, Birth_country, Country_code, Discipline_id)
    VALUES (%s, %s, %s, %s, %s, %s,%s); 
    """
    cursor.execute(query, (Athlete_name, Short_name, Gender, Birth_place,Birth_country, Country_code,Discipline_id))
    
    conn.commit()

        # Close the database connection
    cursor.close()
    conn.close()

        # Redirect back to the countries page
    return "<script>alert('Country added successfully!'); window.location.href='/athletes';</script>"

@app.route('/update_athlete', methods=['POST'])
def update_athlete():
    Athlete_name = request.form.get('athlete_name')
    Short_name = request.form.get('short_name')
    Gender = request.form.get('gender')
    Birth_place = request.form.get('birth_place')
    Birth_country = request.form.get('birth_country')
    Country_code = request.form.get('country_code')
    Discipline = request.form.get('discipline')

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update athlete information
    query = """
    UPDATE athletes
    SET Athlete_name = %s, Short_name = %s, Gender = %s, Birth_place = %s, 
        Birth_country = %s, Country_code = %s, Discipline_id = %s
    WHERE Athlete_id = %s;
    """
    athlete_id = request.args.get('id')  # Assuming the athlete ID is passed in the URL
    cursor.execute(query, (Athlete_name, Short_name, Gender, Birth_place, Birth_country, Country_code, Discipline, athlete_id))

    # Update Discipline_id by joining with the discipline table

    # Commit changes
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return redirect(url_for('athletes'))

@app.route('/discipline', methods=['GET'])
def discipline():
    discipline_name = request.args.get('discipline')
    # Connect to the database and retrieve disciplines data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if discipline_name:
        cursor.execute("SELECT * FROM discipline WHERE Discipline_id = %s", (discipline_name,))
    else:
        cursor.execute("SELECT * FROM discipline")
    disciplines = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('discipline.html', disciplines=disciplines)

@app.route('/delete_discipline>', methods=['POST'])
def delete_discipline():
    Discipline_id = request.args.get('discipline')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM discipline WHERE Discipline_id = %s", (Discipline_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('discipline')) # No content response

@app.route('/insert_discipline', methods=['POST'])
def insert_discipline():
    # Retrieve form data
    discipline = request.form.get('discipline')
    F = int(request.form.get('F'))
    M = int(request.form.get('M'))
    Total = F + M

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

        # Insert data into the database
    query = """
    INSERT INTO discipline (Discipline, F, M, Total)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (discipline, F, M, Total))
    conn.commit()

        # Close the database connection
    cursor.close()
    conn.close()

        # Redirect back to the discipline page
    return "<script>alert('Discipline added successfully!'); window.location.href='/discipline';</script>"

@app.route('/update_discipline', methods=['POST'])
def update_discipline():
    # Retrieve form data
    discipline_id = request.form.get('discipline_id')
    discipline = request.form.get('discipline')
    F = int(request.form.get('F'))
    M = int(request.form.get('M'))
    Total = F + M

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE discipline
    SET Discipline = %s,
        F = %s,
        M = %s,
        Total = %s
    WHERE Discipline_id = %s
    """

    cursor.execute(query, (discipline, F, M, Total, discipline_id))

    # Commit the changes
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return "<script>alert('Discipline updated successfully!'); window.location.href='/discipline';</script>"


@app.route('/events', methods=['GET'])
def events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    event_id = request.args.get('events')

    if event_id:
        cursor.execute("SELECT * FROM events_ WHERE event_id = %s", (event_id,))
    else:
        cursor.execute("SELECT * FROM events_")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('events.html', events=events)

@app.route('/update_event', methods=['POST'])
def update_event():
    # Retrieve form data
    Event_stage = request.form.get('event_stage')
    Event_id = request.args.get('event')
    Location = request.form.get('location')
    Event_status = request.form.get('event_status')
    Time = request.form.get('time')
    Discipline_id = request.form.get('discipline')

    # Insert the new event into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    UPDATE events_ 
    SET Event_Stage = COALESCE(%s, Event_stage), 
    Location = COALESCE(%s, Location),
    Event_status = COALESCE(%s, Event_status), 
    Time = COALESCE(%s, Time), 
    Discipline_id = COALESCE(%s, Discipline_id)
    WHERE Event_id = %s
    """
    cursor.execute(query, ( Event_stage, Location,  Event_status, Time, Discipline_id,Event_id))
    
    conn.commit()
    cursor.close()
    conn.close()

    # Redirect back to the events page
    return "<script>alert('Event updated successfully!'); window.location.href='/events';</script>"

@app.route('/delete_event>', methods=['POST'])
def delete_event():
    event_id = request.args.get('events')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events_ WHERE Event_id = %s", (event_id,))
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
    discipline_id = request.form.get('discipline_id')

    # Insert the new event into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO events_ (Event_stage, Location, Event_status, Time, Discipline_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (event_stage, location, event_status, time, discipline_id))
    
    conn.commit()
    cursor.close()
    conn.close()

    # Redirect back to the events page
    return "<script>alert('Event added successfully!'); window.location.href='/events';</script>"

if __name__ == '__main__':
    app.run(debug=True)



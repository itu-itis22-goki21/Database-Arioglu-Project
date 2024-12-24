from flask import Blueprint, render_template, redirect, url_for, request
from app.db import get_db_connection

coaches_bp = Blueprint('coaches', __name__)

@coaches_bp.route('/coaches', methods=['GET'])
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

@coaches_bp.route('/delete_coaches>', methods=['POST'])
def delete_coaches():
    Coach_id = request.args.get('coaches')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coaches WHERE Coach_id = %s", (Coach_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('coaches.coaches'))

@coaches_bp.route('/insert_coach', methods=['POST'])
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
    return redirect(url_for('coaches.coaches'))

@coaches_bp.route('/update_coach', methods=['POST'])
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
    return redirect(url_for('coaches.coaches'))
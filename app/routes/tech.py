from flask import Blueprint, render_template, redirect, url_for, request
from app.db import get_db_connection

tech_bp = Blueprint('tech', __name__)

@tech_bp.route('/tech')
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


@tech_bp.route('/delete_tech>', methods=['POST'])
def delete_tech():
    tech_id = request.args.get('tech')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tech_of WHERE Tech_id = %s", (tech_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('tech.tech')) # No content response

@tech_bp.route('/insert_tech', methods=['POST'])
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
    return redirect(url_for('tech.tech'))

@tech_bp.route('/update_tech', methods=['POST'])
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

    return redirect(url_for('tech.tech'))
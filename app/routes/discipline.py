from flask import Blueprint, render_template, redirect, url_for, request
from app.db import get_db_connection

discipline_bp = Blueprint('discipline', __name__)

@discipline_bp.route('/discipline', methods=['GET'])
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

@discipline_bp.route('/delete_discipline>', methods=['POST'])
def delete_discipline():
    Discipline_id = request.args.get('discipline')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM discipline WHERE Discipline_id = %s", (Discipline_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('discipline.discipline')) # No content response

@discipline_bp.route('/insert_discipline', methods=['POST'])
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
    return redirect(url_for('discipline.discipline'))

@discipline_bp.route('/update_discipline', methods=['POST'])
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

    return redirect(url_for('discipline.discipline'))
from flask import Blueprint, render_template, redirect, url_for, request
from app.db import get_db_connection

medal_bp = Blueprint('medal', __name__)

@medal_bp.route('/medal', methods=['GET'])
def medal():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get the search query and sort_by parameters from the URL
    search_query = request.args.get('name')  # None if no query is provided
    sort_by = request.args.get('sort_by', 'Athlete_name')  # Default sorting by Athlete_name

    # Validate the sort_by parameter to prevent SQL injection
    valid_sort_columns = {'Athlete_name', 'Medal_code', 'Country_code'}
    if sort_by not in valid_sort_columns:
        sort_by = 'Athlete_name'
    
    # Base query
    base_query = """
        SELECT m.*, a.Athlete_name AS Athlete_name
        FROM medal m
        JOIN athletes a ON m.Athlete_id = a.Athlete_id
    """
    query_params = []

    # Add search filter if search_query exists
    if search_query:
        base_query += " WHERE a.Athlete_name LIKE %s"
        query_params.append('%' + search_query + '%')

    # Add ORDER BY clause for sorting
    if sort_by == 'Medal_code':
        base_query += f" ORDER BY {sort_by} ASC"
    else:
        base_query += f" ORDER BY {sort_by} ASC"

    # Execute the query
    cursor.execute(base_query, tuple(query_params))
    medals = cursor.fetchall()

    # Close database connections
    cursor.close()
    conn.close()

    return render_template("medals.html", medals=medals)



@medal_bp.route('/delete_medal>', methods=['POST'])
def delete_medal():
    medal_id = request.args.get('medal')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medal WHERE Medal_id = %s", (medal_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('medal.medal')) # No content response

@medal_bp.route('/insert_medal', methods=['POST'])
def insert_medal():
    # Retrieve form data
    Medal_type = request.form.get('medal_type')
    Athlete_id = request.form.get('athlete_id')
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
    INSERT INTO medal (Medal_type, Medal_code, Athlete_sex, Event_id, Country_code, Medal_date, Athlete_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (Medal_type, Medal_code, Athlete_sex, Event_id, Country_code, Medal_date, Athlete_id))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect back to the medals page with a success message
    return redirect(url_for('medal.medal'))

@medal_bp.route('/update_medal', methods=['POST'])
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
    return redirect(url_for('medal.medal'))
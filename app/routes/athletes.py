from flask import Blueprint, render_template, redirect, url_for, request
from app.db import get_db_connection
import math
athletes_bp = Blueprint('athletes', __name__)

@athletes_bp.route('/athletes', methods=['GET'])
def athletes():
    # Get the current page number from the URL, default to page 1
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page

    # Retrieve filters and sorting from the query parameters
    athlete_id = request.args.get('athletes')
    country_code = request.args.get('country_code')
    athlete_name = request.args.get('athlete_name')
    sort_by = request.args.get('sort_by', 'Athlete_id')  # Default to sort by Athlete_id

    # Validate the sort_by input to prevent SQL injection
    valid_sort_columns = {'Athlete_id', 'Country_code', 'Athlete_name', 'Discipline_id'}
    if sort_by not in valid_sort_columns:
        sort_by = 'Athlete_id'

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Base query and parameters
    base_query = "SELECT * FROM athletes"
    count_query = "SELECT COUNT(*) FROM athletes"
    where_clauses = []
    query_params = []

    # Add filters based on query parameters
    if athlete_id:
        where_clauses.append("Athlete_id = %s")
        query_params.append(athlete_id)
    if country_code:
        where_clauses.append("Country_code = %s")
        query_params.append(country_code)
    if athlete_name:
        where_clauses.append("Athlete_name LIKE %s")
        query_params.append(f"%{athlete_name}%")  # Use wildcard for partial matches

    # Construct WHERE clause if there are filters
    if where_clauses:
        where_clause = " WHERE " + " AND ".join(where_clauses)
        base_query += where_clause
        count_query += where_clause

    # Get the total count of athletes for pagination
    cursor.execute(count_query, tuple(query_params))
    total_athletes = cursor.fetchone()['COUNT(*)']
    total_pages = math.ceil(total_athletes / per_page)

    # Add ORDER BY clause for sorting
    base_query += f" ORDER BY {sort_by}"

    # Fetch athletes with pagination
    base_query += " LIMIT %s OFFSET %s"
    query_params.extend([per_page, offset])
    cursor.execute(base_query, tuple(query_params))
    athletes = cursor.fetchall()

    # Close database connections
    cursor.close()
    conn.close()

    # Render the athletes page
    return render_template(
        'athletes.html',
        athletes=athletes,
        page=page,
        total_pages=total_pages,
        country_code=country_code,
        athlete_name=athlete_name
    )


@athletes_bp.route('/delete_athlete>', methods=['POST'])
def delete_athlete():
    Athlete_id = request.args.get('athletes')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM athletes WHERE Athlete_id = %s", (Athlete_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('athletes.athletes')) # No content response

@athletes_bp.route('/insert_athlete', methods=['POST'])
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
    return redirect(url_for('athletes.athletes'))

@athletes_bp.route('/update_athlete', methods=['POST'])
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

    return redirect(url_for('athletes.athletes'))
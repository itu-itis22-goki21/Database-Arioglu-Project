from flask import Blueprint, render_template, redirect, url_for, request
from app.db import get_db_connection

country_bp = Blueprint('country', __name__)

@country_bp.route('/country', methods=['GET'])
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

@country_bp.route('/delete_country>', methods=['POST'])
def delete_country():
    country = request.args.get('country')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM country WHERE Country_code = %s", (country,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('country.country')) # No content response

@country_bp.route('/insert_country', methods=['POST'])
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
    return redirect(url_for('country.country'))

@country_bp.route('/update_country', methods=['POST'])
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

    return redirect(url_for('country.country'))
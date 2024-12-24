from flask import Blueprint, render_template, redirect, url_for, request
from app.db import get_db_connection

statistic_bp = Blueprint('statistic', __name__)

@statistic_bp.route('/statistic', methods=['GET'])
def statistic():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            a.Athlete_id, 
            a.Athlete_name, 
            SUM(
                CASE 
                    WHEN m.Medal_type = 'Gold' THEN 3
                    WHEN m.Medal_type = 'Silver' THEN 2
                    WHEN m.Medal_type = 'Bronze' THEN 1
                    ELSE 0
                END
            ) AS Medal_Points,
            COUNT(m.Medal_id) AS Medal_Count
        FROM 
            athletes a 
        JOIN 
            medal m ON a.Athlete_id = m.Athlete_id
        GROUP BY 
            a.Athlete_id, 
            a.Athlete_name
        HAVING 
            Medal_Points > 0
        ORDER BY 
            Medal_Points DESC, Medal_Count DESC;
    """
    
    cursor.execute(query)
    statistic = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('statistic.html', statistic=statistic)
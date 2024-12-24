from flask import Blueprint, render_template, redirect, url_for, request
from app.db import get_db_connection

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET'])
def events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    event_id = request.args.get('events')
    search_query = request.args.get('search')
    discipline_id = request.args.get('discipline')

    sql_query = "SELECT * FROM events_ WHERE 1=1"
    params = []

    # Filter by event_id if provided
    if event_id:
        sql_query += " AND event_id = %s"
        params.append(event_id)

    # Filter by Event_stage if search_query is provided
    if search_query:
        sql_query += " AND Event_stage LIKE %s"
        params.append('%' + search_query + '%')

    # Filter by Discipline_id if provided
    if discipline_id:
        sql_query += " AND Discipline_id = %s"
        params.append(discipline_id)

    # Execute the query with parameters
    cursor.execute(sql_query, tuple(params))
    events = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('events.html', events=events)


@events_bp.route('/update_event', methods=['POST'])
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
    return redirect(url_for('events.events'))

@events_bp.route('/delete_event>', methods=['POST'])
def delete_event():
    event_id = request.args.get('events')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events_ WHERE Event_id = %s", (event_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('events.events'))

@events_bp.route('/insert_event', methods=['POST'])
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
    return redirect(url_for('events.events'))
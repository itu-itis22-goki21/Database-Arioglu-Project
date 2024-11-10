



@app.route("/medal")
def medal_page():
    conn = get_db_connection()




    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medal")  # Ensure that the table name is correct
    medals = cursor.fetchall()


        
    cursor.close()


    
    conn.close()


    return render_template("medals.html", medals=medals)


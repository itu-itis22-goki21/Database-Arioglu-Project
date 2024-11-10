from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': "test"
}
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/")
def medal_page():
    conn = get_db_connection()




    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medal")  # Ensure that the table name is correct
    medals = cursor.fetchall()


        
    cursor.close()


    
    conn.close()


    return render_template("medals.html", medals=medals)
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import mysql.connector
from flask import request, jsonify

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': "test"
}

# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def coaches():
    # Connect to the database and retrieve coaches data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM coaches")
    coaches = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Render the coaches page with the fetched data
    return render_template('flcoaches.html', coaches=coaches)



# Update Coach
@app.route('/coaches/update/<int:id>', methods=['POST'])
def update_coach(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE coaches SET name = %s, experience = %s WHERE id = %s"
    cursor.execute(query, (data.get('name'), data.get('experience'), id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Coach updated successfully"}), 200

# Delete Coach
@app.route('/coaches/delete/<int:id>', methods=['POST'])
def delete_coach(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coaches WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Coach deleted successfully"}), 200

# Filter Coaches
@app.route('/coaches/filter', methods=['GET'])
def filter_coaches():
    experience = request.args.get('experience')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM coaches WHERE experience = %s", (experience,))
    coaches = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(coaches)

# Order Coaches
@app.route('/coaches/order', methods=['GET'])
def order_coaches():
    order_by = request.args.get('order_by', 'name')  # default to ordering by name
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM coaches ORDER BY {order_by}")
    coaches = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(coaches)

if __name__ == '__main__':
    app.run(debug=True)
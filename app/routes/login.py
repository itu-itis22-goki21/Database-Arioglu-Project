from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.db import get_db_connection

login_bp = Blueprint('login', __name__)

# Login and Registration Route
@login_bp.route('/', methods=['GET', 'POST']) 
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'login' in request.form:  # If the login form is submitted
            email = request.form.get('email')
            password = request.form.get('password')

            # Raw SQL query to validate user credentials
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            result = cursor.fetchone()

            if result:  # If user exists
                flash("Login successful!", "success")
                return redirect(url_for("main.home"))  # Redirect to home page
            else:
                flash("Invalid email or password.", "danger")
            
            cursor.close()
            conn.close()

        elif 'register' in request.form:  # If the registration form is submitted
            email = request.form.get('reg_email')
            password = request.form.get('reg_password')
            name = request.form.get('reg_name')

            # Check if the email already exists
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Email already registered. Please log in.", "warning")
            else:
                # Insert the new user into the database
                cursor.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)", (email, password, name))
                conn.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("login.login"))  # Redirect back to login page

            cursor.close()
            conn.close()

    return render_template("login.html")  # Render login page

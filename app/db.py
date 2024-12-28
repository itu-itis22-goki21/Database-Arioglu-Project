import mysql.connector

db_config = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    'database': "database"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
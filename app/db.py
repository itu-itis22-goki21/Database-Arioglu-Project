import mysql.connector

db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': "test"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
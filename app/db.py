import mysql.connector

db_config = {
    'user': 'root',
    'password': 'Qweasdqwe123.',
    'host': 'localhost',
    'database': "database"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
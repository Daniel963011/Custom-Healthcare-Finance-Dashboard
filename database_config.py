import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host = 'localhost',
        user = '',
        password = '',
        database = 'healthcare_finance'
    )

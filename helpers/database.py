import sqlite3

connection: object = sqlite3.connect('database.db')
cursor: object = connection.cursor()

class Database:
    def create_table():
        cursor.execute("CREATE TABLE IF NOT EXISTS sessions (id_hash VARCHAR(255), approx_last_used_time VARCHAR(255), operating_system VARCHAR(255), platform VARCHAR(255))")
        connection.commit()
        
    def get_sessions():
        cursor.execute("SELECT id_hash FROM sessions")
        return cursor.fetchall()
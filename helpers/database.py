import sqlite3

connection: object = sqlite3.connect('database.db')
cursor: object = connection.cursor()

class Database:
    def create_table():
        cursor.execute("CREATE TABLE IF NOT EXISTS sessions (id_hash TEXT, approx_last_used_time TEXT, operating_system TEXT, platform TEXT)")
        connection.commit()
import sqlite3

connection: object = sqlite3.connect('database.db')
cursor: object = connection.cursor()

class Database:
    def create_table():
        cursor.execute("CREATE TABLE IF NOT EXISTS sessions (id_hash VARCHAR(255), operating_system VARCHAR(255), platform VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS account_information (email VARCHAR(255), password VARCHAR(255), token VARCHAR(255)))")
        # cursor.execute("CREATE TABLE IF NOT EXISTS backup_codes (code VARCHAR(255))")
        connection.commit()
        
    def get_sessions():
        return_array: list[str] = []
        
        result = cursor.execute("SELECT id_hash FROM sessions").fetchall()
        result_length: int = len(result)
        
        for i in range(result_length):
            return_array.append(result[i][0])
        
        return return_array
    
    def add_session(id_hash: str, operating_system: str, platform: str):
        cursor.execute("INSERT INTO sessions VALUES (?, ?, ?)", (id_hash, operating_system, platform))
        connection.commit()
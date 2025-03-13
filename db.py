import sqlite3

DB_PATH = "workout2.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def obter_usuario_id(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

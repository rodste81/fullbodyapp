import sqlite3

DB_PATH = "workout2.db"

def get_connection():
    return sqlite3.connect(DB_PATH)
    
def obter_usuario_id(username):
    """Retorna o ID do usuário a partir do username"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None
    
def criar_banco():
    """Cria as tabelas do banco de dados se não existirem."""
    conn = get_connection()
    cursor = conn.cursor()

   cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        grupo TEXT NOT NULL,
        UNIQUE(usuario_id, nome, grupo),  -- 🔥 Garante que um mesmo exercício não será cadastrado duas vezes
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')

    # Criando a tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL
    )''')

    # Criando a tabela de exercícios associada ao usuário
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        grupo TEXT NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')

    # Criando a tabela de treinos associada ao usuário
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS treinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        dia TEXT NOT NULL,
        grupo TEXT NOT NULL,
        exercicio TEXT NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')

    conn.commit()
    conn.close()


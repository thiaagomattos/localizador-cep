import sqlite3

DB_NAME = "enderecos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enderecos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cep TEXT NOT NULL,
            rua TEXT NOT NULL,
            numero INTEGER,
            complemento TEXT,
            bairro TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)
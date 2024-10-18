import sqlite3

def create_connection():
    conn = sqlite3.connect("SAM_DATABASE.db")
    return conn

print("Conectado ao banco de dados...")


def create_user_table():
    conn = sqlite3.connect("SAM_DATABASE.db")
    cursor = conn.cursor()

    # Cria uma tabela para o usuário
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users(
                   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE,
                   password TEXT
                   )
                ''')

    # Cria tabela de arquivos    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS files(
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT
                )
            ''')
    
    # Cria tabela de arquivos do usuário
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_files(
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                filename TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
    
    conn.commit()
    conn.close()

create_user_table()

def insert_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username,password) VALUES (?,?)', (username, password))
    conn.commit()
    conn.close()

def insert_softwares(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO files (name) VALUES (?)',(name,))
    conn.commit()
    conn.close()

def insert_user_files(user_id, filename):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_files (user_id, filename) VALUES (?, ?)', (user_id, filename))
    conn.commit()
    conn.close()


def get_user_files(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM user_files WHERE user_id = ?", (user_id,))
    user_files = cursor.fetchall()
    conn.close()
    return [file[0] for file in user_files]

def get_user_id(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None
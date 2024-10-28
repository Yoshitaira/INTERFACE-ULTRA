import sqlite3
import hashlib

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

def insert_softwares(file_id, filename):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO files (file_id, filename) VALUES (?,?)',(file_id,filename,))
    conn.commit()
    conn.close()

def insert_user_files(user_id, filename):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_files (user_id, filename) VALUES (?, ?)', (user_id, filename))
    conn.commit()
    conn.close()

def delete_user_files(user_id, filename):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_files WHERE user_id = ? AND filename = ?', (user_id,filename))
    conn.commit()
    conn.close()

def get_user_files(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT uf.filename
                   FROM user_files uf
                   JOIN users u ON uf.user_id = u.user_id
                   WHERE u.username= ?""", (username,))
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

def get_user_password(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    password = cursor.fetchone()
    conn.close()
    return password[0] if username else None

def get_all_files():
    conn = create_connection()
    cursor  =conn.cursor()
    cursor.execute("SELECT filename FROM files")
    files = cursor.fetchall()
    conn.close()
    return files
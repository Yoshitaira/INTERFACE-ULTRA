import hashlib
import binascii
# Básicos
import sqlite3
from databaset import create_connection, insert_user, get_user_id, insert_user_files
from tkinter import messagebox


# ---------------------- REGISTRO DE USUÁRIOS E SOFTWARES -----------------------------------
# criptografando as senhas 
def hash_password(password):
    """Gera uma senha hash SHA-256 da senha."""
    return hashlib.sha256(password.encode()).hexdigest()
# autenticação de usuário
def user_register(username, password, filenames):
    if username and password:
        hashed_password = hash_password(password)
        conn = create_connection()
        try:
            insert_user(username, hashed_password)
            user_id = get_user_id(username)
            if user_id is not None:
                for filename in filenames:
                    insert_user_files(user_id, filename)

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "User already exists.")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Fill in all fields.")

def  get_selected_files(check_vars, softwares):
    """Retorna uma lista de arquivos correspondentes aos checkboxes marcados."""
    selected_files = []
    for var, software in zip(check_vars, softwares):
        if var.get():
            selected_files.append(software+".ps1")
    return selected_files
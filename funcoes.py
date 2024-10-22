import hashlib
import subprocess
# Básicos
#import sqlite3
from databaset import *
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


#--------------------------------------- Login do usuário -------------------------------------
def verify_user(username, password):
    """Autentica um usuário verificando as credenciais."""
    pass_hash = hash_password(password)
    stored_password = get_user_password(username)

    print(f"Senha fornecida: {pass_hash}")
    print(f"Senha armazenada: {stored_password}")

    if stored_password and stored_password == pass_hash:
        return True
    return False

# ------------------------------------- Executa scripts do powershell -------------------------
software_scripts ={
    "7zip": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\7zip.ps1",
    "Adobe": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Adobe.ps1",
    "Bullzip": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Bullzip.ps1",
    "Chrome": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Chrome.ps1",
    "DesignReview": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\DesignReview.ps1",
    "DWGTrueView": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\DWGTrueView.ps1",
    "Earth": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Earth.ps1",
    "Java": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Java.ps1",
    "Lightshot": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Lightshot.ps1",
    "NextCloud": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\NextCloud.ps1",
    "PDFSam": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\PDFSam.ps1",
    "QGIS": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\QGIS.ps1"  
}

# Função para executar os scripts do PowerShell
def run_power_shell_scripts(selected_softwares):
    for software in selected_softwares:
        script_path = software_scripts.get(software)
        if not script_path:
            messagebox.showwarning("Warning", f"No script found for {software}.")
            continue
        try:
            print(f"Executando script: {script_path}")
            result = subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True, capture_output=True, text=True)
            print(result.stdout)  # Mostra a saída do script
            messagebox.showinfo("Success", f"Script for {software} executed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Erro: {e.stderr}")  # Mostra o erro do script
            messagebox.showerror("Error", f"Error executing script for {software}: {e}")

def install_selected(softwares, check_vars):
    print(f"Length of softwares: {len(softwares)}")
    print(f"Length of check_vars: {len(check_vars)}")
    
    selected_softwares = [
        software for i, software in enumerate(softwares)
        if i < len(check_vars) and check_vars[i].get()
    ]
    
    if selected_softwares:
        run_power_shell_scripts(selected_softwares)
    else:
        messagebox.showwarning("Selection Error", "No software selected.")


import hashlib
import subprocess
import os
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
            selected_files.append(software)
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
    "Easy2": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Easy2.ps1",
    "FortiClient": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\FortiClient.ps1",
    "FoxitReader": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\FoxitReader.ps1",
    "Java": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Java.ps1",
    "Lightshot": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Lightshot.ps1",
    "NextCloud": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\NextCloud.ps1",
    "OwnCloud": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\OwnCloud.ps1",
    "PDFSam": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\PDFSam.ps1",
    "QGIS": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\QGIS.ps1",
    "RocketChat": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\RocketChat.ps1",
    "Teams": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Teams.ps1",
    "TrimbleConnect": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\TrimbleConnect.ps1",
    "Zoom": "C:\\Users\\Paulo\\Desktop\\Projeto - Instalador Ultra\\instalador\\Zoom.ps1",
}

# Função para executar os scripts do PowerShell
def run_power_shell_scripts(selected_softwares):
    print(f"Available scripts: {list(software_scripts.keys())}")
    for software in selected_softwares:
        #normalized_software = software.strip().lower()
        script_path = software_scripts.get(software)
        print(f"Checking script for: {software}")
        if not script_path:
            messagebox.showwarning("Warning", f"No script found for {software}.")
            continue
        try:
            print(f"Executando script: {script_path}")
            command = f"Start-Process powershell.exe -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\"' -Verb RunAs"
            result = subprocess.run(["powershell.exe", "-Command", command], check=True, capture_output=True, text=True)
            print(result.stdout)
            messagebox.showinfo("Success", f"Script for {software} executed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Erro: {e.stderr}")
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

    print(f"Selected softwares for installation: {selected_softwares}")


# ------------------------------------ Tela de catalogos --------------------------------------------
# Função para adicionar os softwares no catalogo do cliente

def add_file_to_user_catalog(user_id,filename):
    insert_user_files(user_id,filename)
    print(f"Added {filename} to {user_id}'s catalog.")

def add_to_user_catalog(tree_db_files, tree_user_files, user_id):
    # Obtém o item selecionado do catálogo Ultra
    selected_item = tree_db_files.selection()
    if not selected_item:
        print("No file selected.")
        return # Adiciona um aviso para o usuário se necessário
    
    file_to_add = tree_db_files.item(selected_item, 'values')[0]

    add_file_to_user_catalog(user_id, file_to_add)

    tree_user_files.insert("", "end", values=(file_to_add,))
    print(f"File '{file_to_add}' added to user catalog.")

def remove_from_user_catalog(tree_user_files, user_id):
    selected_item = tree_user_files.selection()
    if not selected_item:
        print("No file selected.")
        return
    
    # Obtém o nome do arquivo a ser removido
    file_to_remove = tree_user_files.item(selected_item,'values')[0]

    # Remove o arquivo do banco de dados
    delete_user_files(user_id,file_to_remove)

    # Remove o arquivo do Treeview do usuário
    tree_user_files.delete(selected_item)
    print(f"File '{file_to_remove}' removed from user catalog.")

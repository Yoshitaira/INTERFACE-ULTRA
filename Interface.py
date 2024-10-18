import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from funcoes import get_selected_files, user_register
from databaset import get_user_files, create_user_table, get_user_id
from tkinter import StringVar
from tkinter import messagebox

app = ttk.Window(themename='cosmo')

class Sistema():
    

    def __init__(self):
        self.app = app
        self.tela_padrao()
        create_user_table()
        self.softwares = [
            "7zip","Adobe Reader","Bullzip","Chrome","DesignReview",
            "DWGTruView","Earth","Easy2","FortiClient","FoxitReader",
            "Java","Lightshot","NextCloud","OwnCloud","PDFSam",
            "QGIS","RocketChat","Teams","TrimbleConnect","Zoom"
        ]  # Nome dos softwares
        self.tela_app()
        app.mainloop()

    def tela_padrao(self):
        self.app.geometry("700x400")
        self.app.title("Ultra SAM - app")
        self.app.resizable(False, False)

    def tela_app(self):
        self.frame_app = ttk.Frame(app, width=650, height=350)
        self.frame_app.pack(pady=20, padx=20)
        
        # widgets de login
        login_label = ttk.Label(self.frame_app, font=("Helvetica", 18), text="Welcome to UltraIT Software and Applications Manager")
        login_label.pack(side=TOP, pady=10)

        # data entry
        username_label = ttk.Label(self.frame_app, text="Username:")
        username_label.pack(pady=5)
        self.user_entry = ttk.Entry(self.frame_app)
        self.user_entry.pack(pady=10)

        password_label = ttk.Label(self.frame_app, text="Password:")
        password_label.pack(pady=5)
        self.pass_entry = ttk.Entry(self.frame_app, show="*")
        self.pass_entry.pack(pady=10)

        # buttons login or register
        login_button = ttk.Button(self.frame_app, text="Sign in", bootstyle="primary", command=self.tela_usuario)
        login_button.pack(pady=10)

        register_button = ttk.Button(self.frame_app, text="Register", bootstyle="dark, outline", command=self.tela_registro)
        register_button.pack(pady=10)

    #tela de registro
    def tela_registro(self):
        self.frame_app.pack_forget()  # Esconde a tela de login
        
        # Cria a tela de registro
        self.frame_reg = ttk.Frame(app, width=650, height=350)
        self.frame_reg.pack(pady=20, padx=20)

        reg_label = ttk.Label(self.frame_reg, font=("Helvetica", 18), text="Register")
        reg_label.grid(row=0, column=0, columnspan=2, pady=10)

        username_label = ttk.Label(self.frame_reg, text="Username:")
        username_label.grid(row=1, column=0, sticky=W, padx=10)
        self.reg_user_entry = StringVar()
        self.reg_user_entry = ttk.Entry(self.frame_reg, textvariable=self.reg_user_entry)
        self.reg_user_entry.grid(row=1, column=1, pady=10)

        password_label = ttk.Label(self.frame_reg, text="Password:")
        password_label.grid(row=2, column=0, sticky=W, padx=10)
        self.reg_pass_entry = StringVar()
        self.reg_pass_entry = ttk.Entry(self.frame_reg, show="*", textvariable=self.reg_pass_entry)
        self.reg_pass_entry.grid(row=2, column=1, pady=5)

       # Lista de softwares
       

        # Adiciona checkboxes para os softwares
        self.check_vars = []
        for i, software in enumerate(self.softwares):
            var = ttk.BooleanVar()
            checkbox = ttk.Checkbutton(self.frame_reg, bootstyle="primary-square-toggle", text=software, variable=var)
            row, col = divmod(i, 5)  # 10 checkboxes por coluna
            checkbox.grid(row=row+3, column=col, sticky=W, padx=10, pady=10)
            self.check_vars.append(var)

        # Botões na parte inferior, centralizados
        button_frame = ttk.Frame(self.frame_reg)
        button_frame.grid(row=3+10, column=0, columnspan=2, pady=20)

        register_button = ttk.Button(button_frame, text="Create Account", bootstyle="primary", command=self.user_register)
        register_button.pack(side=LEFT, padx=10)

        back_button = ttk.Button(button_frame, text="Back to Login", bootstyle="dark, outline", command=self.voltar_login)
        back_button.pack(side=LEFT, padx=10)

    def user_register(self):
        username = self.reg_user_entry.get()
        password = self.reg_pass_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        selected_files = get_selected_files(self.check_vars, self.softwares)
        
        try:
            user_register(username, password, selected_files)  # Apenas username e password agora
            # Aqui você pode armazenar selected_files se necessário
            messagebox.showinfo("Success", "User registered successfully!")
            self.voltar_login()
        except ValueError as ve:
            messagebox.showerror("Registration Error", str(ve))
        except RuntimeError as re:
            messagebox.showerror("Database Error", str(re))

    # Tela de usuário
    def tela_usuario(self):
        self.frame_app.pack_forget()
        self.frame_user = ttk.Frame(app, width=650, height=350)
        self.frame_user.pack(pady=20, padx=20)

        user_label = ttk.Label(self.frame_user, font=("Helvetica", 18), text="Management panel of ???")
        user_label.grid(row=0, column=0, columnspan=2, pady=10)

        username = self.user_entry.get() 
        user_id = get_user_id(username) # Obtém o nome de usuário da tela de login
        user_files = get_user_files(user_id)  # Recupera os arquivos do banco de dados

        user_label = ttk.Label(self.frame_user, font=("Helvetica", 18), text=f"Management panel for {username}")
        user_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Adiciona checkboxes para os softwares
        self.check_vars = []
        num_columns = 5  # Número de colunas
        for i, software in enumerate(self.softwares):
            var = ttk.BooleanVar(value=software in user_files)  # Marca o checkbox se o software estiver na lista
            checkbox = ttk.Checkbutton(self.frame_user, text=software, variable=var)
            self.check_vars.append(var)

            # Calcula a linha e a coluna para o grid
            row = i // num_columns  # Linha atual
            col = i % num_columns   # Coluna atual
            checkbox.grid(row=row + 1, column=col, sticky=W, padx=10, pady=5)

        # Botões na parte inferior, centralizados
        button_frame = ttk.Frame(self.frame_user)
        button_frame.grid(row=3+10, column=0,sticky=W, columnspan=3, pady=20)

        download_button = ttk.Button(button_frame, text="Install", bootstyle="primary")
        download_button.pack(side=LEFT, padx=10)

        uninstall_button = ttk.Button(button_frame, text="Uninstall", bootstyle="danger")
        uninstall_button.pack(side=LEFT, padx=10)

        back_button = ttk.Button(button_frame, text="Exit", bootstyle="dark, outline", command=self.voltar_login)
        back_button.pack(side=LEFT, padx=10)

    def voltar_login(self):
        self._clear_current_frame()  # Esconde a tela atual
        self.tela_app()  # Chama a função para exibir a tela de login novamente

    def _clear_current_frame(self):
        """Esconde a tela atual."""
        for widget in self.app.winfo_children():
            widget.pack_forget()

Sistema()

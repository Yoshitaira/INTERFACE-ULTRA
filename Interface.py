import ttkbootstrap as ttk
import time
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from funcoes import *
from databaset import *
from tkinter import StringVar
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import PhotoImage

app = ttk.Window(themename='cosmo')

class Sistema():


    def __init__(self):
        self.app = app
        self.tela_padrao()
        create_user_table()
        self.softwares = [
            "7zip","Adobe","Bullzip","Chrome","DesignReview",
            "DWGTruView","Earth","Easy2","FortiClient","FoxitReader",
            "Java","Lightshot","NextCloud","OwnCloud","PDFSam",
            "QGIS","RocketChat","Teams","TrimbleConnect","Zoom"
        ]  # Nome dos softwares
        self.tela_app()
        # self.load_image()
        app.mainloop()

    def tela_padrao(self):
        self.app.geometry("700x400")
        self.app.title("Ultra SAM - app")
        self.app.resizable(False, False)

    def tela_app(self):
        self.frame_app = ttk.Frame(app, width=650, height=350)
        self.frame_app.pack(pady=20, padx=20)

        # widgets de login
        login_label = ttk.Label(self.frame_app, font=("", 18), text=f"Welcome to UltraIT \n Software and Applications Manager", anchor=CENTER)
        login_label.pack(pady=10)

        # data entry
        username_label = ttk.Label(self.frame_app, text="Username:")
        username_label.pack(pady=5)
        self.user_entry = StringVar()
        self.user_entry = ttk.Entry(self.frame_app, textvariable=self.user_entry)
        self.user_entry.pack(pady=10)

        password_label = ttk.Label(self.frame_app, text="Password:")
        password_label.pack(pady=5)
        self.pass_entry = StringVar()
        self.pass_entry = ttk.Entry(self.frame_app, show="*", textvariable=self.user_entry)
        self.pass_entry.pack(pady=10)

        # buttons login or register
        login_button = ttk.Button(self.frame_app, text="Sign in", bootstyle="primary", command=self.user_login_entry)
        login_button.pack(pady=10)

        register_button = ttk.Button(self.frame_app, text="Register", bootstyle="dark, outline", command=self.tela_registro)
        register_button.pack(pady=10)
        
    def user_login_entry(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        
        if verify_user(username, password):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.tela_usuario()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos.")

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

        username = self.user_entry.get() 
        #user_id = get_user_id(username) # Obtém o nome de usuário da tela de login
        user_files = get_user_files(username)  # Recupera os arquivos do banco de dados
        print(f"User files retrieved: {user_files}")
        #user_files = [file.strip().lower() for file in get_user_files(username)]

        user_label = ttk.Label(self.frame_user, font=("Helvetica", 18), text=f"Management panel for {username}")
        user_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Adiciona checkboxes para os softwares
        self.check_vars = []
        row = 1
        col = 0
        for file in user_files:  # Itera apenas sobre os softwares que o usuário possui
            var = ttk.BooleanVar(value=False)  # Checkbox marcado se está no banco
            checkbox = ttk.Checkbutton(self.frame_user, text=file, variable=var, bootstyle="primary-square-toggle")
            self.check_vars.append(var)
            checkbox.grid(row=row, column=col, sticky=W, padx=10, pady = 10)

            col += 1
            if col == 4:  # Muda para a próxima linha após 5 colunas
                col = 0
                row += 1

        # Botões na parte inferior, centralizados
        button_frame = ttk.Frame(self.frame_user)
        button_frame.grid(row=3+10, column=0,sticky=W, columnspan=3, pady=20)

        download_button = ttk.Button(button_frame, text="Install", bootstyle="primary", command=lambda: install_selected(user_files, self.check_vars))
        download_button.pack(side=ttk.LEFT, padx=10)

        add_button = ttk.Button(button_frame, text="Add a software", bootstyle="Success", command=self.tela_add)
        add_button.pack(side=ttk.LEFT, padx=10)

        back_button = ttk.Button(button_frame, text="Exit", bootstyle="dark, outline", command=self.voltar_login)
        back_button.pack(side=ttk.LEFT, padx=10)
    
    # Tela adicionar software no caálogo de instalação
    def tela_add(self):
        self._clear_current_frame()
        self.frame_add = ttk.Frame(app, width=650, height=350)
        self.frame_add.pack(pady=20, padx=20)

        username = self.user_entry.get() 
        #user_id = get_user_id(username) # Obtém o nome de usuário da tela de login
        user_files = get_user_files(username)  # Recupera os arquivos do banco de dados
        print(f"User files retrieved: {user_files}")
        #user_files = [file.strip().lower() for file in get_user_files(username)]
        user_label = ttk.Label(self.frame_add, font=("Helvetica", 18), text=f"Management panel for {username}")
        user_label.grid(row=0, column=0, columnspan=2, pady=10)

             # Treeview para arquivos do banco de dados
        self.tree_db_files = ttk.Treeview(self.frame_add, columns=("filename"), show='headings')
        self.tree_db_files.heading("filename", text="ULTRA IT CATALOG")
        self.tree_db_files.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Adiciona os arquivos do banco de dados no Treeview
        all_files = get_all_files()
        for file in all_files:
            self.tree_db_files.insert("", "end", values=file)

        # Treeview para arquivos do usuário
        self.tree_user_files = ttk.Treeview(self.frame_add, columns=("filename",), show='headings')
        self.tree_user_files.heading("filename", text=f"{username} CATALOG")
        self.tree_user_files.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Adiciona os arquivos do usuário no Treeview
        for file in user_files:
            self.tree_user_files.insert("", "end", values=(file,))

        # Botões na parte inferior
        button_frame = ttk.Frame(self.frame_add)
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)

        add_button = ttk.Button(button_frame, text="Add to User", bootstyle="primary")
        add_button.pack(side=ttk.LEFT, padx=10)

        remove_button = ttk.Button(button_frame, text="Remove from User", bootstyle="danger")
        remove_button.pack(side=ttk.LEFT, padx=10)

        back_button = ttk.Button(button_frame, text="Back", command=self.voltar_login, bootstyle="dark-outline")
        back_button.pack(side=ttk.LEFT, padx=10)

        self.frame_add.columnconfigure(0, weight=1)  # Deixa a primeira coluna expandível
        self.frame_add.columnconfigure(1, weight=1)  # Deixa a segunda coluna expandível

    # Tela progresso de instalação
    # def tela_instalacao(self, selected_softwares):
    #     self._clear_current_frame()
    #     self.frame_install = ttk.Frame(app, width=650, height=350)
    #     self.frame_install.pack(pady=20, padx=20)

    #     install_label = ttk.Label(self.frame_install, font=("Helvetica", 18), text="Installing Softwares...")
    #     install_label.pack(pady=10)

    #     self.progress_var = ttk.IntVar()
    #     self.progress_bar = ttk.Progressbar(self.frame_install, variable =self.progress_var, maximum=len(selected_softwares), bootstyle="primary")
    #     self.progress_bar.pack(padx=20, pady=20)
    #     self.progress_bar.config(length=300)

    #     run_power_shell_scripts(selected_softwares, self.progress_var)

    def voltar_login(self):
        # self.show_progress_bar()
        # self.update_progress_bar()
        self._clear_current_frame()  # Esconde a tela atual
        self.tela_app()  # Chama a função para exibir a tela de login novamente

    def _clear_current_frame(self):
        """Esconde a tela atual."""
        for widget in self.app.winfo_children():
            widget.pack_forget()
    
    # Mostra barra de progresso
    def show_progress_bar(self):
        if hasattr(self, 'progress_bar'):
            self.progress_bar.pack_forget()
        
        self.progress_var = ttk.IntVar()
        self.progress_bar = ttk.Progressbar(self.app, variable=self.progress_var, maximum=100, bootstyle="primary")
        self.progress_bar.pack(pady=20, padx=20)
        self.progress_bar.config(length=300)

    def update_progress_bar(self):
        for i in range(101):
            self.progress_var.set(i)  # Atualiza o valor da barra de progresso
            self.app.update_idletasks()  # Atualiza a interface
            time.sleep(0.05)  # Ajuste o tempo conforme necessário

    # def load_image(self):
    #     image_path = "C:\Users\Paulo\Desktop\Projeto - Instalador Ultra\LOGO ULTRA.png"
    #     img = Image.open(image_path)
    #     img = img.resize((200, 100), Image.ANTIALIAS)  # Redimensionar a imagem se necessário
    #     self.photo = ImageTk.PhotoImage(img)

    #     self.label = ttk.Label(self.frame_app, image=self.photo)
    #     self.label.pack()

Sistema()

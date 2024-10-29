import ttkbootstrap as ttk
import time
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from funcoes import *
from databaset import *
from tkinter import StringVar, messagebox, CENTER, PhotoImage
from PIL import Image, ImageTk

app = ttk.Window(themename='cosmo')

class Sistema():

    def __init__(self):
        self.app = app
        self.tela_padrao()
        create_user_table()
        self.softwares = [
            "7zip","Adobe","Bullzip","Chrome","DesignReview",
            "DWGTrueView","Earth","Easy2","FortiClient","FoxitReader",
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

    # Tela de login
    def tela_app(self):
        self.frame_app = ttk.Frame(app, width=700, height=400)
        self.frame_app.pack(pady=20, padx=20)
        style = ttk.Style()

        # Adiciona a imagem
        try:
            original_image = Image.open(r"C:\Users\Paulo\Desktop\Projeto - Instalador Ultra\logo1.png")
            self.logo_image = original_image.resize((248, 100), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(self.logo_image)

            logo_label = ttk.Label(self.frame_app, image=self.logo_image)
            logo_label.place(x=43, y=28)  # Posição no canto superior esquerdo
        except Exception as e:
            print(f"Error loading image: {e}")

        # widgets de login
        login_label = ttk.Label(self.frame_app, font=("Calibri Light Italic", 18), text=f"WELCOME TO\nSOFTWARE AND\nAPPLICATIONS\nMANAGER. \nWE'RE HERE TO\nHELP YOU.")
        login_label.place(x=73, y=144)  # Posição no canto superior direito

        # data entry
        username_label = ttk.Label(self.frame_app, text="Username:", font=("Calibri", 11))
        username_label.place(x=341, y=60)  # Ajuste a posição conforme necessário 
        self.user_entry = StringVar()
        self.user_entry = ttk.Entry(self.frame_app, textvariable=self.user_entry)
        self.user_entry.place(x=420, y=58, width=200)  # Ajuste a posição e largura conforme necessário

        password_label = ttk.Label(self.frame_app, text="Password:", font=("Calibri", 11))
        password_label.place(x=341, y=126)  # Ajuste a posição conforme necessário
        self.pass_entry = StringVar()
        self.pass_entry = ttk.Entry(self.frame_app,show="*", textvariable=self.user_entry)
        self.pass_entry.place(x=420, y=124, width=200)  # Ajuste a posição e largura conforme necessário

        style.configure("TButton", background="#1E519F", foreground="#FFFFFF",padding=5, font=("Bahnschrift SemiBold", 9),borderwidth=0)
        # buttons login or register
        login_button = ttk.Button(self.frame_app, text="SIGN IN",style="TButton", command=self.user_login_entry)
        login_button.place(x=484, y=200, width=80, height=30)  # Ajuste a posição conforme necessário

        register_button = ttk.Button(self.frame_app, text="REGISTER", bootstyle="dark, outline", command=self.tela_registro)
        register_button.place(x=484, y=260, width=80, height=30)  # Ajuste a posição conforme necessário
    
    def user_login_entry(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        
        if verify_user(username, password):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.tela_usuario()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos.")

    # Tela de registro
    def tela_registro(self):
        self.frame_app.pack_forget()  # Esconde a tela de login
        
        # Cria a tela de registro
        self.frame_reg = ttk.Frame(app, width=700, height=400)
        self.frame_reg.pack(pady=20, padx=20)

        style = ttk.Style()

        # Adiciona a imagem
        try:
            original_image = Image.open(r"C:\Users\Paulo\Desktop\Projeto - Instalador Ultra\logo1.png")
            self.logo_image = original_image.resize((248, 100), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(self.logo_image)

            logo_label = ttk.Label(self.frame_reg, image=self.logo_image)
            logo_label.place(x=43, y=28)  # Posição no canto superior esquerdo
        except Exception as e:
            print(f"Error loading image: {e}")

        username_label = ttk.Label(self.frame_reg, text="Username:",font=("Calibri", 11))
        username_label.place(x=341, y=60)  # Posição no canto superior esquerdo
        self.reg_user_entry = StringVar()
        self.reg_user_entry = ttk.Entry(self.frame_reg, textvariable=self.reg_user_entry)
        self.reg_user_entry.place(x=420, y=58, width=200)

        password_label = ttk.Label(self.frame_reg, text="Password:",font=("Calibri", 11))
        password_label.place(x=341, y=126)
        self.reg_pass_entry = StringVar()
        self.reg_pass_entry = ttk.Entry(self.frame_reg, show="*", textvariable=self.reg_pass_entry)
        self.reg_pass_entry.place(x=420, y=124, width=200)

       # Lista de softwares
        # style.configure("Custom.TCheckbutton", font=("Calibri", 10))
        # Adiciona checkboxes para os softwares
        self.check_vars = []
        checkbox_frame = ttk.Frame(self.frame_reg)
        checkbox_frame.place(x=50, y=180)  # Centraliza o frame de checkboxes

        for i, software in enumerate(self.softwares):
            var = ttk.BooleanVar()
            checkbox = ttk.Checkbutton(checkbox_frame, text=software, variable=var,bootstyle="primary-square-toggle" )
            checkbox.grid(row=i // 5, column=i % 5, sticky='w', padx=10, pady=5)  # 5 checkboxes por linha
            self.check_vars.append(var)

        style.configure("TButton", background="#1E519F", foreground="#FFFFFF",padding=5, font=("Bahnschrift SemiBold", 9),borderwidth=0)
        # Botões
        register_button = ttk.Button(self.frame_reg, text="CREATE ACCONT",style="TButton", command=self.user_register)
        register_button.place(x=168, y=315, width=170, height=30)

        back_button = ttk.Button(self.frame_reg, text="BACK TO LOGIN", command=self.voltar_login,bootstyle="dark, outline")
        back_button.place(x=362, y=315, width=170, height=30)

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
        self.frame_user = ttk.Frame(app, width=700, height=400)
        self.frame_user.pack(pady=20, padx=20)
        style = ttk.Style()

        # Adiciona a imagem
        try:
            original_image = Image.open(r"C:\Users\Paulo\Desktop\Projeto - Instalador Ultra\logo1.png")
            self.logo_image = original_image.resize((248, 100), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(self.logo_image)

            logo_label = ttk.Label(self.frame_user, image=self.logo_image)
            logo_label.place(x=43, y=28)  # Posição no canto superior esquerdo
        except Exception as e:
            print(f"Error loading image: {e}")

        username = self.user_entry.get() 
        #user_id = get_user_id(username) # Obtém o nome de usuário da tela de login
        user_files = get_user_files(username)  # Recupera os arquivos do banco de dados
        print(f"User files retrieved: {user_files}")
        #user_files = [file.strip().lower() for file in get_user_files(username)]

        user_label = ttk.Label(self.frame_user, font=("Bahnschrift SemiBold", 16), text=f"MANAGEMENT PANEL")
        user_label.place(x=375, y=45)
        user_label1 = ttk.Label(self.frame_user, font=("Bahnschrift SemiBold Condensed", 20), text=f"{username}")
        user_label1.place(x=470, y=80)

        # Frame para checkboxes
        checkbox_frame = ttk.Frame(self.frame_user)
        checkbox_frame.place(x=50, y=160)  # Centraliza o frame

        # Adiciona checkboxes para os softwares
        self.check_vars = []
        for i, file in enumerate(user_files):  # Itera apenas sobre os softwares que o usuário possui
            var = ttk.BooleanVar(value=False)  # Checkbox marcado se está no banco
            checkbox = ttk.Checkbutton(checkbox_frame, text=file, variable=var, bootstyle="primary-square-toggle")
            self.check_vars.append(var)
            checkbox.grid(row=i // 5, column=i % 5, sticky='w', padx=10, pady=5)

        style.configure("install.TButton", background="#1E519F", foreground="#FFFFFF", padding=5, font=("Bahnschrift SemiBold", 9),borderwidth=0)
        # Defina um segundo estilo, se necessário
        style.configure("add.TButton", background="#40A919", foreground="#FFFFFF", padding=5, font=("Bahnschrift SemiBold", 9),borderwidth=0)

        # Botões
        download_button = ttk.Button(self.frame_user, text="INSTALL", style="install.TButton", command=lambda: install_selected(user_files, self.check_vars))
        download_button.place(x=50, y=300, width=170, height=30)

        add_button = ttk.Button(self.frame_user, text="ADD A SOFTWARE", style="add.TButton", command=self.tela_add)
        add_button.place(x=255, y=300, width=170, height=30)

        back_button = ttk.Button(self.frame_user, text="EXIT", bootstyle="dark,outline", command=self.voltar_login)
        back_button.place(x=460, y=300, width=170, height=30)

    # Tela adicionar software no catálogo de instalação
    def tela_add(self):
        self._clear_current_frame()
        self.frame_add = ttk.Frame(app, width=700, height=400)
        self.frame_add.pack(pady=20, padx=20)
        style = ttk.Style()

        # Adiciona a imagem
        try:
            original_image = Image.open(r"C:\Users\Paulo\Desktop\Projeto - Instalador Ultra\logo1.png")
            self.logo_image = original_image.resize((248, 100), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(self.logo_image)

            logo_label = ttk.Label(self.frame_add, image=self.logo_image)
            logo_label.place(x=43, y=10)  # Posição no canto superior esquerdo
        except Exception as e:
            print(f"Error loading image: {e}")

        username = self.user_entry.get() 
        #user_id = get_user_id(username) # Obtém o nome de usuário da tela de login
        user_files = get_user_files(username)  # Recupera os arquivos do banco de dados
        print(f"User files retrieved: {user_files}")
        user_id = get_user_id(username)
        user_label = ttk.Label(self.frame_add, font=("Bahnschrift SemiBold", 16), text=f"MANAGEMENT PANEL")
        user_label.place(x=390, y=35)
        user_label1 = ttk.Label(self.frame_add, font=("Bahnschrift SemiBold Condensed", 20), text=f"{username}")
        user_label1.place(x=490, y=70)

        style.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=25,fieldbackground="#1E519F")
        style.configure("Treeview.Heading",background="#1E519F",foreground="#FFFFFF",font=("Bahnschrift SemiBold", 10))
        # Treeview para arquivos do banco de dados
        self.tree_db_files = ttk.Treeview(self.frame_add, columns=("filename"), show='headings', style="Treeview")
        self.tree_db_files.heading("filename", text="ULTRA IT CATALOG")
        self.tree_db_files.place(x=41, y=130, width=270, height=200)

        # Adiciona os arquivos do banco de dados no Treeview
        all_files = get_all_files()
        for file in all_files:
            self.tree_db_files.insert("", "end", values=file)

        # Treeview para arquivos do usuário
        self.tree_user_files = ttk.Treeview(self.frame_add, columns=("filename",), show='headings', style="Treeview")
        self.tree_user_files.heading("filename", text=f"{username} CATALOG")
        self.tree_user_files.place(x=377, y=130, width=260, height=150)

        # Adiciona os arquivos do usuário no Treeview
        for file in user_files:
            self.tree_user_files.insert("", "end", values=(file,))

        style.configure("add.TButton", background="#40A919", foreground="#FFFFFF", padding=5, font=("Bahnschrift SemiBold", 9),borderwidth=0)
        # Defina um segundo estilo, se necessário
        style.configure("remove.TButton", background="#A91919", foreground="#FFFFFF", padding=5, font=("Bahnschrift SemiBold", 9),borderwidth=0)

        add_button = ttk.Button(self.frame_add, text="ADD", style="add.TButton", command=lambda: add_to_user_catalog(self.tree_db_files, self.tree_user_files, user_id))
        add_button.place(x=377, y=300, width=70, height=30)

        remove_button = ttk.Button(self.frame_add, text="REMOVE", style="remove.TButton", command=lambda:remove_from_user_catalog(self.tree_user_files, user_id))
        remove_button.place(x=457, y=300, width=70, height=30)

        back_button = ttk.Button(self.frame_add, text="BACK", command=self.voltar_tela_user, bootstyle="dark-outline")
        back_button.place(x=537, y=300, width=100, height=30)

        self.frame_add.columnconfigure(0, weight=1)  # Deixa a primeira coluna expandível
        self.frame_add.columnconfigure(1, weight=1)  # Deixa a segunda coluna expandível

    # Botões de voltar 
    def voltar_login(self):
        # self.show_progress_bar()
        # self.update_progress_bar()
        self._clear_current_frame()  # Esconde a tela atual
        self.tela_app()  # Chama a função para exibir a tela de login novamente
    
    def voltar_tela_user(self):
        self._clear_current_frame()  # Esconde a tela atual
        self.tela_usuario()  # Chama a função para exibir a tela de login novamente

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

Sistema()

import customtkinter as ctk

from gui.main_window import MainWindow
from gui.register_window import RegisterWindow
from user import User


class LoginWindow:
    def __init__(self, master, database):
        self.master = master
        self.master.title("Logowanie")
        self.master.geometry("400x300")
        self.database = database

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.username_label = ctk.CTkLabel(self.frame, text="Nazwa użytkownika")
        self.username_label.pack(pady=12, padx=10)
        self.username_entry = ctk.CTkEntry(self.frame)
        self.username_entry.pack(pady=12, padx=10)

        self.password_label = ctk.CTkLabel(self.frame, text="Hasło")
        self.password_label.pack(pady=12, padx=10)
        self.password_entry = ctk.CTkEntry(self.frame, show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(self.frame, text="Zaloguj", command=self.login)
        self.login_button.pack(pady=12, padx=10)

        self.register_button = ctk.CTkButton(self.frame, text="Zarejestruj", command=self.open_register_window)
        self.register_button.pack(pady=12, padx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = User(username, password)
        if user.login(self.database):
            self.master.destroy()
            root = ctk.CTk()
            app = MainWindow(root, user, self.database)
            root.mainloop()

    def open_register_window(self):
        root = ctk.CTk()
        app = RegisterWindow(root, self.database)
        root.mainloop()

import customtkinter as ctk

from user import User


class RegisterWindow:
    def __init__(self, master, database):
        self.master = master
        self.master.title("Rejestracja")
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

        self.register_button = ctk.CTkButton(self.frame, text="Zarejestruj", command=self.register)
        self.register_button.pack(pady=12, padx=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = User(username, password)
        user.register(self.database)
        self.master.destroy()
from tkinter import messagebox

from gui import const
from gui.const import *


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.username}"

    def register(self, database):
        try:
            database.add_user(self.username, self.password)
            messagebox.showinfo("Success", "Registration successful")
            print("Registration successful")
        except ValueError as e:
            messagebox.showerror("Failed", str(e))
            print("Registration failed")

    def login(self, database):
        if database.get_user(self.username, self.password):
            const.LOGGED_IN = True
            print(const.LOGGED_IN)
            return True
        else:
            messagebox.showerror("Error", "Invalid username or password")
            return False



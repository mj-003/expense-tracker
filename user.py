from tkinter import messagebox


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self, database):
        try:
            database.add_user(self.username, self.password)
            # messagebox.showinfo("Success", "Registration successful")
            print("Registration successful")
        except ValueError as e:
            # messagebox.showerror("Failed", str(e))
            print("Registration failed")

    def login(self, database):
        if database.get_user(self.username, self.password):
            return True
        else:
            # messagebox.showerror("Error", "Invalid username or password")
            print("Invalid username or password")
            return False

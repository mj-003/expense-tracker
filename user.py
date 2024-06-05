from tkinter import messagebox


class User:
    def __init__(self, username, password, email, id=None):
        self.username = username
        self.password = password
        self.email = email
        self.id = id

    def __str__(self):
        return f"{self.username}"

    def register(self, database):
        try:
            self.id = database.add_user(self.username, self.password, self.email)
            messagebox.showinfo("Success", "Registration successful")
        except ValueError as e:
            messagebox.showerror("Failed", str(e))

    def login(self, database):
        user_data = database.get_user(self.username, self.password)
        if user_data:
            self.id = user_data[0]
            return True
        else:
            messagebox.showerror("Error", "Invalid username or password")
            return False

from tkinter import messagebox


class User:
    def __init__(self, username, password, email, database, currency='PLN', id=None):
        self.username = username
        self.password = password
        self.email = email
        self.id = id
        self.database = database
        self.currency = currency

    def __str__(self):
        return f"{self.username}"

    def register(self):
        try:
            self.id = self.database.add_user(self.username, self.password, self.email, self.currency)
            messagebox.showinfo("Success", "Registration successful")
        except ValueError as e:
            messagebox.showerror("Failed", str(e))

    def login(self):
        user_data = self.database.get_user(self.username, self.password)
        if user_data:
            self.id = user_data[0]
            return True
        else:
            messagebox.showerror("Error", "Invalid username or password")
            return False

    def change_password(self, new_password):
        self.database.change_password(self.username, new_password)
        self.password = new_password

    def change_email(self, new_email):
        self.database.change_email(self.username, new_email)
        self.email = new_email

    def change_currency(self, new_currency):
        self.database.change_currency(self.username, new_currency)
        self.currency = new_currency

from tkinter import messagebox


class User:
    """
    Class User.

    This class is responsible for managing the user's data.
    The user can register, login, change password, change email, change currency.

    """
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
        """

        Register the user. If the user is already registered, it will raise an error.

        """
        try:
            self.id = self.database.add_user(self.username, self.password, self.email, self.currency)
            messagebox.showinfo("Success", "Registration successful")
        except ValueError as e:
            messagebox.showerror("Failed", str(e))

    def login(self):
        """

        Login the user. If the user is not registered, it will raise an error.

        """
        user_data = self.database.get_user(self.username, self.password)
        if user_data:
            self.id = user_data[0]
            return True
        else:
            messagebox.showerror("Error", "Invalid username or password")
            return False

    def change_password(self, new_password):
        """

        Change the current user's password to a new one.

        :param new_password: new password provided by the user.
        :return: None

        """
        self.database.change_password(self.username, new_password)
        self.password = new_password

    def change_email(self, new_email):
        """

        Change the user's email to a new one.

        :param new_email: new email provided by the user.
        :return: None

        """
        self.database.change_email(self.username, new_email)
        self.email = new_email

    def change_currency(self, new_currency):
        """

        Change the user's current currency.

        :param new_currency: new currency provided by the user.
        :return: None

        """
        self.database.change_currency(self.username, new_currency)
        self.currency = new_currency

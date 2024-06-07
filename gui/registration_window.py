from tkinter import messagebox

from PIL import Image
from customtkinter import *

from user import User


class RegistrationWindow(CTkToplevel):
    """

    Class RegistrationWindow.

    This class is responsible for the registration window.
    It enables the user to register a new account.
    If user already has an account, they can login instead.

    To register, the user must provide:
    - Email
    - Username
    - Password

    """
    def __init__(self, parent, database):
        super().__init__(parent)

        self.password_entry = None
        self.username_entry = None
        self.email_entry = None

        self.title("Register")
        self.geometry("500x350")

        self.database = database
        self.parent = parent

        self.email_icon = CTkImage(dark_image=Image.open("images/login.png"), size=(20, 20))
        self.password_icon = CTkImage(dark_image=Image.open("images/password.png"), size=(17, 17))

        self.add_register_fields()
        self.add_register_button()

    def add_register_fields(self):
        """

        Add the registration fields.
        The fields are:
        - Email
        - Username
        - Password

        """
        register_frame = CTkFrame(master=self, fg_color="transparent")
        register_frame.pack(anchor="center", pady=(50, 0))

        CTkLabel(master=register_frame, text="Email:", text_color="#4b6053", anchor="w", justify="left",
                 font=("Aptos", 14), image=self.email_icon, compound="left").pack(
            anchor="w", padx=(0, 0))

        self.email_entry = CTkEntry(master=register_frame, width=225, fg_color="#EEEEEE",
                                    border_color="#4b6053",
                                    border_width=1, text_color="#000000")
        self.email_entry.pack(anchor="w", pady=(7, 0))

        CTkLabel(master=register_frame, text="Username:", text_color="#4b6053", anchor="w", justify="left",
                 font=("Aptos", 14), image=self.email_icon, compound="left").pack(
            anchor="w", padx=(0, 0))

        self.username_entry = CTkEntry(master=register_frame, width=225, fg_color="#EEEEEE",
                                       border_color="#4b6053",
                                       border_width=1, text_color="#000000")
        self.username_entry.pack(anchor="w", pady=(7, 0))

        CTkLabel(master=register_frame, text="Password:", text_color="#4b6053", anchor="w", justify="left",
                 font=("Aptos", 14), image=self.password_icon, compound="left").pack(
            anchor="w", padx=(0, 0))

        self.password_entry = CTkEntry(master=register_frame, width=225, fg_color="#EEEEEE",
                                       border_color="#4b6053",
                                       border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", pady=(7, 0))

    def add_register_button(self):
        """

        Add the register button.

        """
        CTkButton(master=self, text="Register", fg_color="#658354", hover_color="#4b6053",
                  font=("Aptos", 12),
                  text_color="#ffffff", width=225, command=self.perform_register).pack(anchor='center', pady=(15, 0))

    def perform_register(self):
        """

        Perform the registration.
        Validate the fields.
        User must provide:
        - Email
        - Username (min 5 characters, max 15 characters)
        - Password (min 5 characters, max 15 characters)

        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        user = User(username=username, password=password, email=email, database=self.database)

        if username and password and email:
            is_ok = True
            if len(password.strip()) < 5:
                is_ok = False
                messagebox.showerror("Error", "Password must be at least 5 characters")

            if len(username.strip()) < 5:
                is_ok = False
                messagebox.showerror("Error", "Username must be at least 5 characters")

            if len(username.strip()) > 15:
                is_ok = False
                messagebox.showerror("Error", "Username must be less than 15 characters")

            if len(password.strip()) > 15:
                is_ok = False
                messagebox.showerror("Error", "Password must be less than 15 characters")

            if is_ok:
                user.register()
                self.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

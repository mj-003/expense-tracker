from tkinter import messagebox

from PIL import Image
from customtkinter import *

from gui.registration_window import RegistrationWindow
from user import User


class LoginPage(CTkFrame):
    def __init__(self, parent, app, database):
        super().__init__(parent)

        self.user_incomes = None
        self.app = app
        self.parent = parent
        self.database = database

        set_appearance_mode("light")

        self.user = None
        self.user_expenses = None
        self.username_entry = None
        self.password_entry = None

        self.frame = None
        self.email_icon = CTkImage(dark_image=Image.open("images/login.png"), size=(20, 20))
        self.password_icon = CTkImage(dark_image=Image.open("images/password.png"), size=(20, 20))

        self.add_image()
        self.add_log_pass()
        self.login()
        self.add_register()

    def add_image(self):
        """
        Add the image to the login page
        :return:
        """
        side_img_data = Image.open("images/green_background3.jpeg")
        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(450, 745))

        CTkLabel(master=self, text="", image=side_img).pack(expand=True, side="left")

    def add_log_pass(self):
        """
        Add the login and password fields
        :return:
        """
        self.frame = CTkFrame(master=self, width=556, height=745)
        self.frame.pack_propagate(False)
        self.frame.pack(expand=True, fill="both", padx=(0, 0))

        CTkLabel(master=self.frame, text="Welcome Back!", text_color="#4b6053", justify="left",
                 font=("Aptos", 35, 'bold')).pack(anchor="w", pady=(100, 5), padx=(150, 0))

        CTkLabel(master=self.frame, text="Sign in to your account", text_color="#75975e", anchor="w", justify="left",
                 font=("Arial Bold", 15)).pack(anchor="w", padx=(150, 0))

        CTkLabel(master=self.frame, text="  Username:", text_color="#658354", anchor="w", justify="left",
                 font=("Aptos", 14), image=self.email_icon, compound="left").pack(anchor="w", pady=(38, 0),
                                                                                  padx=(150, 0))

        self.username_entry = CTkEntry(master=self.frame, width=255, fg_color="#EEEEEE", border_color="#4b6053",
                                       border_width=1, text_color="#000000", placeholder_text='Your username')
        self.username_entry.pack(anchor="w", padx=(150, 0))

        CTkLabel(master=self.frame, text="  Password:", text_color="#658354", anchor="w", justify="left",
                 font=("Aptos", 14), image=self.password_icon, compound="left").pack(anchor="w", pady=(21, 0),
                                                                                     padx=(150, 0))

        self.password_entry = CTkEntry(master=self.frame, width=255, fg_color="#EEEEEE", border_color="#4b6053",
                                       border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=(150, 0))

    def login(self):
        """
        Add the login button
        :return:
        """
        CTkButton(master=self.frame, text="Login", fg_color="#658354", hover_color="#4b6053", font=("Aptos", 12),
                  text_color="#ffffff", width=255, command=self.perform_login).pack(anchor="w", pady=(40, 0),
                                                                                    padx=(150, 0))

    def perform_login(self):
        """
        Perform the login
        :return:
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
        elif not self.database.get_user(username, password):
            messagebox.showerror("Error", "Invalid username or password")
        else:
            id, us, pas, em, cur = self.database.get_user(username, password)
            self.user = User(username=username, password=password, email=em, id=id, database=self.database, currency=cur)

            if self.user.login():
                self.app.after_logged_in(self.user)

    def add_register(self):
        """
        Add the register button
        :return:
        """
        CTkButton(master=self.frame, text="Register", fg_color="#658354", hover_color="#4b6053",
                  font=("Aptos", 12),
                  text_color="#ffffff", width=255, command=self.show_register_window).pack(anchor="w", pady=(15, 0),
                                                                                           padx=(150, 0))

    def show_register_window(self):
        """
        Show the register window
        :return:
        """
        register_window = RegistrationWindow(self, self.database)
        register_window.grab_set()

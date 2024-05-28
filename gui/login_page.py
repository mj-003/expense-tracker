from PIL import Image
from customtkinter import *
from registration_window import RegistrationWindow
from user import User


class LoginPage(CTkFrame):
    def __init__(self, parent, app, database):
        super().__init__(parent)

        self.app = app
        self.parent = parent
        self.database = database

        self.user = None
        self.username_entry = None
        self.password_entry = None

        self.frame = None
        self.email_icon = CTkImage(dark_image=Image.open("images/email-icon.png"), size=(20, 20))
        self.password_icon = CTkImage(dark_image=Image.open("images/password-icon.png"), size=(17, 17))

        self.add_image()
        self.add_log_pass()
        self.login()
        self.add_register()

    def add_image(self):
        side_img_data = Image.open("images/side-img.png")
        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(400, 745))

        CTkLabel(master=self, text="", image=side_img).pack(expand=True, side="left")

    def add_log_pass(self):
        self.frame = CTkFrame(master=self, width=556, height=745, fg_color="#ffffff")
        self.frame.pack_propagate(False)
        self.frame.pack(expand=True, side="right")

        CTkLabel(master=self.frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left",
                 font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

        CTkLabel(master=self.frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left",
                 font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=self.frame, text="  Email:", text_color="#601E88", anchor="w", justify="left",
                 font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))

        self.username_entry = CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                       border_width=1, text_color="#000000")
        self.username_entry.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=self.frame, text="  Password:", text_color="#601E88", anchor="w", justify="left",
                 font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))

        self.password_entry = CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                       border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=(25, 0))

    def login(self):
        CTkButton(master=self.frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225, command=self.perform_login).pack(anchor="w", pady=(40, 0), padx=(25, 0))

    def perform_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.user = User(username, password)

        if self.user.login(self.database):
            self.app.after_logged_in(self.user)

    def add_register(self):
        CTkButton(master=self.frame, text="Register", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225, command=self.show_register_window).pack(anchor="w", pady=(15, 0), padx=(25, 0))

    def show_register_window(self):
        register_window = RegistrationWindow(self, self.database)
        register_window.grab_set()


from tkinter import messagebox

from PIL import Image
from customtkinter import *

from user import User


class RegistrationWindow(CTkToplevel):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.password_entry = None
        self.username_entry = None
        self.title("Register")
        self.geometry("500x300")

        self.database = database
        self.parent = parent

        self.email_icon = CTkImage(dark_image=Image.open("images/email-icon.png"), size=(20, 20))
        self.password_icon = CTkImage(dark_image=Image.open("images/password-icon.png"), size=(17, 17))

        self.add_register_fields()
        self.add_register_button()

    def add_register_fields(self):
        register_frame = CTkFrame(master=self, fg_color="transparent")
        register_frame.pack(anchor="center", pady=(50, 0))

        CTkLabel(master=register_frame, text="Email:", text_color="#601E88", anchor="w", justify="left",
                 font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(
            anchor="w", padx=(0, 0))

        self.username_entry = CTkEntry(master=register_frame, width=225, fg_color="#EEEEEE",
                                       border_color="#601E88",
                                       border_width=1, text_color="#000000")
        self.username_entry.pack(anchor="w", pady=(5, 0))

        CTkLabel(master=register_frame, text="Password:", text_color="#601E88", anchor="w", justify="left",
                 font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(
            anchor="w", padx=(0, 0))

        self.password_entry = CTkEntry(master=register_frame, width=225, fg_color="#EEEEEE",
                                       border_color="#601E88",
                                       border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", pady=(5, 0))

    def add_register_button(self):
        CTkButton(master=self, text="Register", fg_color="#601E88", hover_color="#E44982",
                  font=("Arial Bold", 12),
                  text_color="#ffffff", width=225, command=self.perform_register).pack(anchor='center', pady=(15, 0))

    def perform_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = User(username, password)

        if username and password:
            user.register(self.database)
            self.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

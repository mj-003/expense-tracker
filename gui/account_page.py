import datetime
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.home_page_controller import HomePageController
from gui.login_page import LoginPage
from plots import MyPlotter
from widgets_and_buttons import *


class AccountPage(CTkFrame):
    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.today = datetime.datetime.today().strftime('%a, %-d.%m')

        self.app = app
        self.parent = parent
        self.user = user

        self.title_frame = None
        self.subtitle_frame = None
        self.options_frame = None
        self.action_frame = None

        self.add_title()
        self.add_subtitle()
        self.add_options()
        self.add_action_frame()
        self.edit_account()

    def add_title(self):
        self.title_frame = CTkFrame(self, fg_color='transparent')
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(25, 0))

        title_label = CTkLabel(self.title_frame, text=f"Your Account", font=("Aptos", 40, 'bold'), text_color="#2A8C55")
        title_label.pack(anchor='nw', side='left')

        today_label = (CTkLabel(self.title_frame, text=f"{self.today}", font=("Aptos", 35), text_color="#2A8C55"))
        today_label.pack(anchor='ne', side='right')

    def add_subtitle(self):
        self.subtitle_frame = CTkFrame(self, fg_color='transparent')
        self.subtitle_frame.pack(anchor="n", fill="x", padx=27, pady=(5, 0))

        subtitle_label = CTkLabel(self.subtitle_frame, text=f"Welcome {self.user.username}! Choose option!", font=("Aptos", 15),
                                  text_color="#2A8C55")
        subtitle_label.pack(anchor='nw', side='left')

        logout_button = (CTkButton(master=self.subtitle_frame,
                  text="Logout",
                  width=100,
                  height=60,
                  font=("Aptos", 16),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  corner_radius=50,
                  command=self.app.log_out))
        logout_button.pack(
            anchor="ne",
            side="right",
            pady=(10, 0))

    def add_options(self):
        self.options_frame = CTkFrame(self, width=200)
        self.options_frame.pack(expand=True, fill="both", padx=27, pady=21, side='left')

        edit_label = CTkLabel(self.options_frame, text="Edit your account", font=("Aptos", 12), text_color="#2A8C55",
                              compound='left')
        edit_label.pack(anchor='nw', side='top', pady=(30, 0), padx=60)
        edit_button = CTkButton(self.options_frame, text="Edit", fg_color='#2A8C55', compound='left',
                                command=self.edit_account)
        edit_button.pack(anchor='nw', side='top', pady=(0, 20), padx=60)

        currency_label = CTkLabel(self.options_frame, text="Change your currency", font=("Aptos", 12), text_color="#2A8C55",
                               compound='left')
        currency_label.pack(anchor='nw', side='top', pady=(0, 0), padx=60)
        currency_button = CTkButton(self.options_frame, text="Currency", fg_color='#2A8C55', command=self.change_currency,
                                 compound='left')
        currency_button.pack(anchor='nw', side='top', pady=(0, 20), padx=60)



    def add_action_frame(self):
        self.action_frame = CTkFrame(master=self, width=500)
        self.action_frame.pack(expand=True, fill="both", pady=20, padx=(0, 27))
        self.action_frame.pack_forget()

    def edit_account(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        edit_label = CTkLabel(self.action_frame, text="Edit your account", font=("Aptos", 20), text_color="#2A8C55")
        edit_label.pack(anchor='n', side='top', pady=(30, 0), padx=125)

        comment_label = CTkLabel(self.action_frame, text="You can change your e-mail or password.", font=("Aptos", 12), text_color="#2A8C55")
        comment_label.pack(anchor='n', side='top', pady=(0, 0), padx=125)

        email_change_label = CTkLabel(self.action_frame, text="Change E-mail:", font=("Aptos", 12, 'bold'), text_color="#2A8C55")
        email_change_label.pack(anchor='nw', side='top', pady=(10, 0), padx=125)
        email_label = CTkLabel(self.action_frame, text="E-mail:", font=("Aptos", 12), text_color="#2A8C55")
        email_label.pack(anchor='nw', side='top', pady=(0, 0), padx=125)

        self.email_entry = CTkEntry(self.action_frame, width=225, fg_color="#EEEEEE", border_color="#4b6053", border_width=1, text_color="#000000")
        self.email_entry.pack(anchor='nw', side='top', pady=(0, 10), padx=125)
        self.email_entry.insert(0, self.user.email)
        self.email_entry.bind("<Return>", self.change_email)

        password_change_label = CTkLabel(self.action_frame, text="Change password:", font=("Aptos", 12, 'bold'),
                                      text_color="#2A8C55")
        password_change_label.pack(anchor='nw', side='top', pady=(10, 0), padx=125)
        password_label = CTkLabel(self.action_frame, text="Current password:", font=("Aptos", 12), text_color="#2A8C55")
        password_label.pack(anchor='nw', side='top', pady=(0, 0), padx=125)

        self.password_entry = CTkEntry(self.action_frame, width=225, fg_color="#EEEEEE", border_color="#4b6053", border_width=1, text_color="#000000", show='*')
        self.password_entry.pack(anchor='nw', side='top', pady=(0, 0), padx=125)

        new_password_label = CTkLabel(self.action_frame, text="New password:", font=("Aptos", 12), text_color="#2A8C55")
        new_password_label.pack(anchor='nw', side='top', pady=(0, 0), padx=125)

        self.new_password_entry = CTkEntry(self.action_frame, width=225, fg_color="#EEEEEE", border_color="#4b6053", border_width=1, text_color="#000000")
        self.new_password_entry.pack(anchor='nw', side='top', pady=(0, 0), padx=125)
        self.new_password_entry.bind("<Return>", self.change_password)

        back_button = CTkButton(self.action_frame, text="Back", fg_color='#2A8C55', width=225, command=self.back_to_options)
        back_button.pack(anchor='nw', side='bottom', pady=(0, 30), padx=125)

        self.action_frame.pack(expand=True, fill="both", pady=20, padx=(0, 27))

    def change_currency(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()

        title_curr_label = CTkLabel(self.action_frame, text="Change your currency", font=("Aptos", 20), text_color="#2A8C55")
        title_curr_label.pack(anchor='n', side='top', pady=(30, 0), padx=130)

        comment_label = CTkLabel(self.action_frame, text="You can change your currency into following ones:", font=("Aptos", 12),
                                 text_color="#2A8C55")
        comment_label.pack(anchor='n', side='top', pady=(0, 20), padx=80)

        # Zmienna do przechowywania wybranej waluty
        self.currency_var = StringVar(value=self.user.currency)

        # Definiowanie dostępnych walut
        currencies = ["PLN", "USD", "EUR", "JPY", "GBP", "AUD"]

        # Tworzenie Radiobuttonów
        for currency in currencies:
            radio = CTkRadioButton(self.action_frame, text=currency, variable=self.currency_var, value=currency, font=("Aptos", 14), border_color="#2A8C55", fg_color="#2A8C55")
            radio.pack(anchor='w', padx=40, pady=5)

        # Przycisk do zapisania wyboru

        back_button = CTkButton(self.action_frame, text="Back", fg_color='#2A8C55', width=225, command=self.back_to_options)
        back_button.pack(anchor='nw', side='bottom', pady=(0, 25), padx=125)

        save_button = CTkButton(self.action_frame, text="Save Currency", fg_color='#2A8C55', width=225,
                                command=self.save_currency)
        save_button.pack(anchor='nw', side='bottom', pady=(0, 14), padx=125)

        self.action_frame.pack(expand=True, fill="both", pady=20, padx=(0, 27))

    def save_currency(self):
        chosen_currency = self.currency_var.get()
        self.user.change_currency(chosen_currency)
        messagebox.showinfo("Currency Changed", f"Your currency has been changed to {chosen_currency}.")

    def change_theme(self):
        pass

    def change_email(self, event=None):
        if self.user.email == self.email_entry.get():
            messagebox.showwarning("Warning", "Please provide a new email.")
        else:
            new_email = self.email_entry.get()
            self.user.change_email(new_email)
            self.email_entry.delete(0, 'end')
            self.email_entry.insert(0, new_email)
            messagebox.showinfo("Success", "Email changed successfully.")

    def change_password(self, event=None):
        if len(self.new_password_entry.get().strip()) < 5:
            messagebox.showwarning("Warning", "Password must be at least 5 characters long.")
        elif self.password_entry.get() == self.user.password:
            new_password = self.new_password_entry.get()
            if new_password == self.user.password:
                messagebox.showwarning("Warning", "New password must be different from the current one.")
            else:
                self.user.change_password(new_password)
                self.password_entry.delete(0, 'end')
                self.new_password_entry.delete(0, 'end')
                messagebox.showinfo("Success", "Password changed successfully.")
        else:
            messagebox.showwarning("Warning", "Please provide a correct current password.")

    def back_to_options(self):
        self.action_frame.pack_forget()




from customtkinter import *
import tkinter as tk
from expenses.expense import Expense
from utils.date_entry import DateEntry


class ExpensePage(CTkFrame):
    def __init__(self, parent, app, database, user):
        super().__init__(parent)

        self.app = app
        self.parent = parent
        self.user = user
        self.database = database

        self.category = None
        self.amount = None
        self.description = None
        self.date = None
        self.payment_method = None
        self.date_entry = None

        self.add_title()
        self.add_fields()
        self.add_buttons()

    def add_title(self):
        CTkLabel(master=self,
                 text="Add expense",
                 font=("Arial Black", 25),
                 text_color="#2A8C55").pack(
            anchor="nw",
            pady=(29, 0),
            padx=27)

    def add_fields(self):
        grid = CTkFrame(master=self, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31, 0))

        # add amount
        CTkLabel(master=grid,
                 text="Amount",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=0,
            column=0,
            sticky="w")

        self.amount = (CTkEntry(master=grid,
                                fg_color="#F0F0F0",
                                border_width=0,
                                width=300))

        self.amount.grid(
            row=1,
            column=0,
            ipady=10)

        # add category
        CTkLabel(master=grid,
                 text="Category",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=0,
            column=1,
            sticky="w",
            padx=(25, 0))

        self.category = CTkComboBox(master=grid, width=300,
                                    values=["Personal", "Home", "Food", "Transport", "Entertainment", "Other"],
                                    button_color="#2A8C55",
                                    border_color="#2A8C55",
                                    button_hover_color="#207244",
                                    dropdown_hover_color="#207244",
                                    dropdown_fg_color="#2A8C55",
                                    dropdown_text_color="#fff",
                                    font=("Arial", 15))

        self.category.grid(
            row=1,
            column=1,
            ipady=10,
            padx=(24, 0),
            pady=15)

        # add description
        CTkLabel(master=grid,
                 text="Description",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=12,
            column=0,
            sticky="w")

        self.description = CTkEntry(master=grid,
                                    fg_color="#F0F0F0",
                                    border_width=0,
                                    border_color="black",

                                    width=300,
                                    height=120)
        self.description.grid(
            row=15,
            column=0,
            ipady=10)

        # add date
        CTkLabel(master=grid,
                 text="Date",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=12,
            column=1,
            sticky="w",
            padx=(25, 0))

        self.date_entry = DateEntry(grid)
        self.date_entry.grid(row=15, column=1, padx=(24, 0), pady=15)

        # add payment method
        CTkLabel(master=grid,
                 text="Payment method",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=30,
            column=0,
            sticky="w")

        self.payment_method = tk.IntVar(value=0)

        CTkRadioButton(master=grid,
                       variable=self.payment_method,
                       value=0,
                       text="Cash",
                       font=("Arial Bold", 14),
                       text_color="#52A476",
                       fg_color="#52A476",
                       border_color="#52A476",
                       hover_color="#207244").grid(
            row=34,
            column=0,
            sticky="w",
            pady=(16, 0))

        CTkRadioButton(master=grid,
                       variable=self.payment_method,
                       value=1,
                       text="Card",
                       font=("Arial Bold", 14),
                       text_color="#52A476",
                       fg_color="#52A476",
                       border_color="#52A476",
                       hover_color="#207244").grid(
            row=35,
            column=0,
            sticky="w",
            pady=(16, 0))

        CTkRadioButton(master=grid,
                       variable=self.payment_method,
                       value=2,
                       text="Online",
                       font=("Arial Bold", 14),
                       text_color="#52A476",
                       fg_color="#52A476",
                       border_color="#52A476",
                       hover_color="#207244").grid(
            row=36,
            column=0,
            sticky="w",
            pady=(16, 0))

    def add_buttons(self):
        CTkButton(master=self,
                  text="BACK",
                  width=150,
                  height=50,
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  font=("Arial Black", 20),
                  command=lambda: self.app.return_to_home_page()).pack(
            side='right',
            ipady=5,
            pady=(0, 0),
            padx=(20, 27))

        CTkButton(master=self,
                  text="ADD",
                  width=150,
                  height=50,
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  font=("Arial Black", 20),
                  command=self.add_expense_to_user).pack(
            side="right",
            ipady=5,
            pady=(0, 0))

    def add_expense_to_user(self):
        # map payment method
        self.payment_method = ["Cash", "Card", "Online"][self.payment_method.get()]

        curr_expense = Expense(self.amount.get(), self.category.get(), self.description.get(),
                               self.payment_method, self.date_entry.date_var.get())

        self.database.add_expense(self.user.id, curr_expense)

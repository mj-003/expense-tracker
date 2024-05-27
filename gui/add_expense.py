from customtkinter import *
import tkinter as tk
from tkcalendar import Calendar
from expenses.expense import Expense


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

        self.add_title()
        self.add_fields()

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
        # CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0, width=300).grid(
        #     row=1,
        #     column=1,
        #     ipady=10,
        #     padx=(24, 0))

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
                                    width=300,
                                    height=140)
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

        calendar = CustomCalendar(grid,
                                  selectmode='day',
                                  year=2022,
                                  month=5,
                                  day=22)
        calendar.configure(background='#52A476', foreground='white')
        calendar.grid(row=15, column=1, padx=(24, 0), pady=15)

        # add payment method
        CTkLabel(master=grid,
                 text="Payment method",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=27,
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
            row=30,
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
            row=31,
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
            row=32,
            column=0,
            sticky="w",
            pady=(16, 0))
        # CTkRadioButton(master=grid, variable=payment_method, value=3, text="Not important", font=("Arial Bold", 14),
        #                text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(
        #     row=33, column=0, sticky="w", pady=(16, 0))

        # add button
        CTkButton(master=self,
                  text="ADD",
                  width=150,
                  height=150,
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  font=("Arial Black", 20),
                  command=self.add_expense_to_user).pack(
            anchor="e",
            ipady=5,
            pady=(0, 25),
            padx=27)

    def add_expense_to_user(self):
        # map payment method
        self.payment_method = ["Cash", "Card", "Online"][self.payment_method.get()]
        print(self.payment_method)

        curr_expense = Expense(self.amount.get(), self.category.get(), self.description.get(),
                               self.payment_method)
        print(curr_expense)
        print(self.database.get_columns())
        self.database.add_expense(self.database.get_user_id(self.user.username), curr_expense)


class CustomCalendar(Calendar):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.configure(background="white", disabledbackground="white", bordercolor="white",
                       headersbackground="green", normalbackground="black", foreground='black',
                       normalforeground='black', headersforeground='black')

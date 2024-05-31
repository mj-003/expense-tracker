from customtkinter import *
import tkinter as tk
from tkinter import filedialog
from financials.expense import Expense
from utils.date_entry import DateEntry
from financials.user_expenses import UserExpenses
from financials.income import Income
from PIL import Image, ImageTk


class IncomePage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent)

        self.app = app
        self.parent = parent
        self.user = user
        self.database = database
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes

        self.amount = None
        self.date = None
        self.from_who = None

        self.add_title()
        self.add_fields()
        self.add_buttons()

    def add_title(self):
        CTkLabel(master=self,
                 text="Add income",
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

        self.amount = CTkEntry(master=grid,
                               fg_color="#F0F0F0",
                               border_width=0,
                               width=300)
        self.amount.grid(
            row=1,
            column=0,
            sticky="w")

        # add from
        CTkLabel(master=grid,
                 text="From",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=2,
            column=0,
            sticky="w")

        self.from_who = CTkEntry(master=grid,
                                 fg_color="#F0F0F0",
                                 border_width=0,
                                 width=300)
        self.from_who.grid(
            row=3,
            column=0,
            sticky="w")

        # add date
        CTkLabel(master=grid,
                 text="Date",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=4,
            column=0,
            sticky="w")

        self.date = CTkEntry(master=grid,
                                 fg_color="#F0F0F0",
                                 border_width=0,
                                 width=300)
        self.date.grid(
            row=5,
            column=0,
            sticky="w")

    def add_buttons(self):
        grid = CTkFrame(master=self, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31, 0))

        # add button
        CTkButton(master=grid,
                  text="Add",
                  font=("Arial", 15),
                  bg_color="#2A8C55",
                  text_color="#fff",
                  width=10,
                  command=self.add_income_to_user
                  ).grid(
            row=0,
            column=0,
            sticky="w")

    def add_income_to_user(self):
        amount = self.amount.get()
        from_who = self.from_who.get()
        date = self.date.get()

        income = Income(amount, from_who, date)
        self.user_incomes.add_income(income)
        print('added income:')
        print(self.user_incomes.get_incomes())
        # print(list(self.user_incomes))
        self.amount.delete(0, 'end')
        self.from_who.delete(0, 'end')
        self.date.delete(0, 'end')


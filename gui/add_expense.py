from customtkinter import *
import tkinter as tk
from tkcalendar import DateEntry


class ExpensePage(CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.parent = parent

        self.add_title()
        self.add_fields()

    def add_title(self):
        CTkLabel(master=self, text="Add expense", font=("Arial Black", 25), text_color="#2A8C55").pack(
            anchor="nw", pady=(29, 0), padx=27)

    def add_fields(self):
        grid = CTkFrame(master=self, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31, 0))

        # add amount
        CTkLabel(master=grid, text="Amount", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(
            row=0,
            column=0,
            sticky="w")
        CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0, width=300).grid(
            row=1,
            column=0,
            ipady=10)

        # add category
        CTkLabel(master=grid, text="Category", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(
            row=0,
            column=1,
            sticky="w",
            padx=(25, 0))
        CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0, width=300).grid(
            row=1,
            column=1,
            ipady=10,
            padx=(24, 0))

        # add description
        CTkLabel(master=grid, text="Description", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(
            row=12,
            column=0,
            sticky="w")
        CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0, width=300).grid(
            row=15,
            column=0,
            ipady=10)

        # add date
        CTkLabel(master=grid, text="Date", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(
            row=12,
            column=1,
            sticky="w",
            padx=(25, 0))

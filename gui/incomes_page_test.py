from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image, ImageTk
from customtkinter import *

from categories import Categories
from financials.expense import Expense
from financials.income import Income
from item_page_abc import FinancialsPage


class IncomesPageTest(FinancialsPage):
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent=parent, app=app, database=database, user=user, user_items=user_expenses,
                         user_items2=user_incomes)
        self.sort_filter = None
        self.category_filter = None
        self.date_filter = None
        self.user_items = user_incomes
        self.user_items_list = user_incomes.get_incomes()
        self.amount_entry = None
        self.from_entry = None
        self.date_entry = None
        self.title = 'Incomes'

        self.create_title_frame(self.show_add_income_form)
        self.create_metrics_frame()
        self.create_search_container_income()
        self.create_info_panel()
        self.show_user_incomes()

    def show_user_incomes(self):
        self.user_items_list = self.user_items.get_incomes()
        self.show_user_items()

    def create_search_container_income(self):
        self.create_search_container()
        CTkButton(master=self.search_container,
                  text='✔',
                  width=30,
                  font=("Aptos", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_more_income_info).pack(
            side="left",
            padx=(13, 0),
            pady=15)

        self.date_filter = CTkComboBox(master=self.search_container,
                                       width=155,
                                       values=["Date", "This month", "This year"],
                                       button_color="#2A8C55",
                                       border_color="#2A8C55",
                                       border_width=2,
                                       button_hover_color="#207244",
                                       dropdown_hover_color="#207244",
                                       dropdown_fg_color="#2A8C55",
                                       dropdown_text_color="#fff")

        self.date_filter.pack(
            side="left",
            padx=(13, 0),
            pady=15)

        self.category_filter = CTkComboBox(master=self.search_container,
                                           width=155,
                                           values=['Category', Categories.TRANSPORT.value, Categories.FOOD.value,
                                                   Categories.ENTERTAINMENT.value,
                                                   Categories.HOME.value, Categories.PERSONAL.value, ],
                                           button_color="#2A8C55",
                                           border_color="#2A8C55",
                                           border_width=2,
                                           button_hover_color="#207244",
                                           dropdown_hover_color="#207244",
                                           dropdown_fg_color="#2A8C55",
                                           dropdown_text_color="#fff")

        self.category_filter.pack(
            side="left",
            padx=(13, 0),
            pady=15)

        self.sort_filter = CTkComboBox(master=self.search_container,
                                       width=155,
                                       values=['Sort', '⬆ Amount', '⬇ Amount', '⬆ Time', '⬇ Time'],
                                       button_color="#2A8C55",
                                       border_color="#2A8C55",
                                       border_width=2,
                                       button_hover_color="#207244",
                                       dropdown_hover_color="#207244",
                                       dropdown_fg_color="#2A8C55",
                                       dropdown_text_color="#fff")

        self.sort_filter.pack(
            side="left",
            padx=(13, 0),
            pady=15)

        CTkButton(master=self.search_container,
                  text='✔',
                  width=30,
                  font=("Aptos", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_filtered_incomes).pack(
            side="left",
            padx=(13, 0),
            pady=15)

    def get_more_income_info(self):
        self.selected_row = int(self.row_id.get()) if self.row_id.get() else 0
        self.item_info = self.user_items.get_incomes()[self.selected_row]
        self.get_more_info()

    def show_add_income_form(self):
        self.show_add_item_form()
        self.amount_entry = CTkEntry(self.info_panel, placeholder_text="Amount", validate='key',
                                     validatecommand=self.vcmd_money)
        self.amount_entry.pack(pady=(15, 10), padx=(10, 10))

        self.from_entry = CTkEntry(self.info_panel, placeholder_text="From")
        self.from_entry.pack(pady=(10, 10), padx=(10, 10))

        self.date_var = StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = CTkEntry(self.info_panel, textvariable=self.date_var, state='readonly', fg_color="white")
        self.date_entry.pack(pady=(10, 10), padx=(10, 10))
        self.date_entry.bind("<Button-1>", self.open_calendar)

        save_button = CTkButton(self.info_panel, text="✔", fg_color="#2A8C55", command=self.validate_and_save, width=40)
        save_button.pack(pady=(10, 10), padx=(35, 2), side='left')

        back_button = CTkButton(self.info_panel, text="✗", fg_color="#2A8C55", command=self.cancel, width=40)
        back_button.pack(pady=(10, 10), padx=(2, 2), side='left')

        cancel_button = CTkButton(self.info_panel, text="↩︎", fg_color="#2A8C55", command=self.go_back, width=40)
        cancel_button.pack(pady=(10, 10), padx=(2, 10), side='left')

        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def validate_and_save(self):
        amount = self.amount_entry.get()
        from_entry = self.from_entry.get()
        date = self.date_var.get()

        if not amount or not from_entry or not date:
            messagebox.showwarning("Warning", "Please fill in all fields.")
        else:
            self.save_new_item()

    def save_new_item(self):
        new_price = self.amount_entry.get()
        new_from = self.from_entry.get()
        new_date = self.date_entry.get()

        self.new_item = Income(amount=new_price, sender=new_from, date=new_date)

        self.amount_entry.delete(0, 'end')
        self.from_entry.delete(0, 'end')

        self.user_items.add_income(self.new_item)
        self.user_items_list = self.user_items.get_incomes()
        self.show_user_items()
        self.app.define_and_pack_frames()

    def edit_item(self):
        self.edit_dialog = ctk.CTkToplevel(self)
        self.edit_dialog.title(f"Edit {self.title}")
        self.edit_dialog.geometry("330x300")
        self.item_info = self.user_items.get_incomes()[self.selected_row]

        CTkLabel(self.edit_dialog, text="Amount:").grid(row=1, column=0, pady=(50, 10), padx=10, sticky="e")
        self.amount_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[1]), validate='key',
                                     validatecommand=self.vcmd_money)
        self.amount_entry.grid(row=1, column=1, pady=(50, 10), padx=12, sticky="w")

        CTkLabel(self.edit_dialog, text="From:").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.from_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[2]))
        self.from_entry.grid(row=2, column=1, pady=(20, 10), padx=12, sticky="w")

        CTkLabel(self.edit_dialog, text="Date:").grid(row=3, column=0, pady=10, padx=10, sticky="e")
        self.date_entry = CTkEntry(self.edit_dialog, textvariable=self.date_var, state='readonly',
                                   fg_color="white")
        self.date_entry.bind("<Button-1>", self.open_calendar)
        self.date_entry.grid(row=3, column=1, pady=10, padx=12, sticky="w")

        save_button = ctk.CTkButton(self.edit_dialog, text="Save",
                                    fg_color="#2A8C55",
                                    command=lambda: self.save_edited_income())
        save_button.grid(row=4, column=0, columnspan=2, pady=20, padx=20, sticky='w')

        cancel_button = ctk.CTkButton(self.edit_dialog, text="Cancel",
                                    fg_color="#2A8C55",
                                    command=lambda: self.go_back())
        cancel_button.grid(row=4, column=1, columnspan=2, pady=20, padx=20, sticky='e')

        self.edit_dialog.columnconfigure(0, weight=1)
        self.edit_dialog.columnconfigure(1, weight=3)
        self.app.update_user_expenses(self.user_items)

    def delete_item(self):
        self.user_items.delete_income(self.selected_row)
        self.user_items_list = self.user_items.get_incomes()
        self.show_user_items()
        self.info_panel.pack_forget()
        self.app.update_user_incomes(self.user_items)

    def get_filtered_incomes(self):
        date = self.date_filter.get()
        category = self.category_filter.get()
        sort = self.sort_filter.get()

        self.user_items_list = self.controller.get_filtered_incomes(date, category, sort)
        print(self.user_items_list)
        self.get_filtered_items()

    def save_edited_income(self):
        new_income = Income(amount=self.amount_entry.get(),
                            sender=self.from_entry.get(),
                            date=self.date_entry.get(),
                            )

        self.user_items.update_user_incomes(self.selected_row, new_income)
        self.user_items_list = self.user_items.get_incomes()
        self.show_user_incomes()
        self.edit_dialog.destroy()


    def cancel(self):
        self.amount_entry.delete(0, 'end')
        self.from_entry.delete(0, 'end')


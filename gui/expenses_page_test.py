from abc import abstractmethod
from datetime import datetime

from financials.expense import Expense
from item_page_abc import FinancialsPage
from customtkinter import *
from categories import Categories
import customtkinter as ctk

import os
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Style

import customtkinter as ctk
from CTkTable import CTkTable
from PIL import Image, ImageTk
from customtkinter import *
from tkcalendar import DateEntry, Calendar

from categories import Categories
from financials.expense import Expense
from gui.add_expense import ExpensePage
from home_page_controller import HomePageController
from gui.add_income import IncomePage


class ExpensePageTest(FinancialsPage):
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent=parent, app=app, database=database, user=user, user_items=user_expenses,
                         user_items2=user_incomes)
        self.sort_filter = None
        self.category_filter = None
        self.date_filter = None
        self.user_items = user_expenses
        self.user_items_list = user_expenses.get_expenses()
        self.amount_entry = None
        self.category_entry = None
        self.date_entry = None
        self.payment_method_entry = None
        self.recipe_entry = None
        self.title = 'Expenses'

        self.create_title_frame(self.show_add_expense_form)

        self.create_metrics_frame()
        self.create_search_container_expense()
        self.create_info_panel()
        self.show_user_expenses()

    def show_user_expenses(self):
        self.user_items_list = self.user_items.get_expenses()
        self.show_user_items()

    def create_search_container_expense(self):
        print('create_search_container_expense')
        self.create_search_container()
        CTkButton(master=self.search_container,
                  text='✔',
                  width=30,
                  font=("Aptos", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_more_expense_info).pack(
            side="left",
            padx=(13, 70),
            pady=15)

        self.date_filter = CTkComboBox(master=self.search_container,
                                       width=130,
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
                                           width=130,
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
                                       width=130,
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
                  command=self.get_filtered_expenses).pack(
            side="left",
            padx=(13, 0),
            pady=15)

    def get_more_expense_info(self):
        self.get_more_info()
        photo_button = CTkButton(self.info_panel, text="📷", fg_color='#2A8C55', text_color='black',
                                 corner_radius=50, width=60,
                                 height=60, command=lambda: self.show_photo())
        photo_button.pack(padx=10, pady=10, fill='both')

    def show_add_expense_form(self):
        self.show_add_item_form()
        self.amount_entry = CTkEntry(self.info_panel, placeholder_text="Price")
        self.amount_entry.pack(pady=(10, 10), padx=(10, 10))

        self.category_entry = CTkComboBox(self.info_panel,
                                          values=['Personal', 'Transport', 'Food', 'Entertainment', 'Home', 'Other'])
        self.category_entry.pack(pady=(10, 10), padx=(10, 10))

        self.date_var = StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = CTkEntry(self.info_panel, textvariable=self.date_var, state='readonly',
                                   fg_color="white")
        self.date_entry.pack(pady=(10, 10), padx=(10, 10))
        self.date_entry.bind("<Button-1>", self.open_calendar)

        self.payment_method_entry = CTkComboBox(self.info_panel, values=['Online', 'Card', 'Cash', 'Other'])
        self.payment_method_entry.pack(pady=(10, 10), padx=(10, 10))

        CTkButton(master=self.info_panel,
                  text="Photo",
                  fg_color="white",
                  hover_color="#207244",
                  font=("Aptos", 12),
                  border_color="#2A8C55",
                  border_width=2,
                  text_color="#2A8C55",
                  text_color_disabled="white",
                  command=self.upload_photo).pack(pady=(10, 10), padx=(10, 10))

        save_button = CTkButton(self.info_panel, text="Save",
                                fg_color="#2A8C55",
                                command=lambda: self.save_new_item())
        save_button.pack(pady=(10, 10), padx=(10, 10))

        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def save_new_item(self):
        print('save_new_expense')
        new_price = self.amount_entry.get()
        new_category = self.category_entry.get()
        new_date = self.date_entry.get()
        new_payment = self.payment_method_entry.get()
        print(new_price, new_category, new_date, new_payment)

        path = self.recipe_entry if self.recipe_entry else None
        self.new_item = Expense(amount=new_price, category=new_category, payment_method=new_payment, date=new_date,
                                photo_path=path)

        self.amount_entry.delete(0, 'end')
        self.recipe_entry = None

        self.user_items.add_expense(self.new_item)
        self.user_items_list = self.user_items.get_expenses()
        self.show_user_items()
        self.app.define_and_pack_frames()

    def edit_item(self):
        self.edit_dialog = ctk.CTkToplevel(self)
        self.edit_dialog.title(f"Edit {self.title}")
        self.edit_dialog.geometry("400x300")
        self.item_info = self.user_items.get_expenses()[self.selected_row]
        CTkLabel(self.edit_dialog, text="Price:").grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.amount_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[1]))
        self.amount_entry.grid(row=1, column=1, pady=(20, 10), padx=10, sticky="w")

        CTkLabel(self.edit_dialog, text="Category:").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.category_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[2]))
        self.category_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        CTkLabel(self.edit_dialog, text="Date:").grid(row=3, column=0, pady=10, padx=10, sticky="e")
        self.date_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[3]))
        self.date_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        CTkLabel(self.edit_dialog, text="Payment method:").grid(row=4, column=0, pady=10, padx=10, sticky="e")
        self.payment_method_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[4]))
        self.payment_method_entry.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        save_button = ctk.CTkButton(self.edit_dialog, text="Save",
                                    fg_color="#2A8C55",
                                    command=lambda: self.save_edited_expense())
        save_button.grid(row=5, column=0, columnspan=2, pady=20, padx=10)

        self.edit_dialog.columnconfigure(0, weight=1)
        self.edit_dialog.columnconfigure(1, weight=3)
        self.app.update_user_expenses(self.user_items)

    def delete_item(self):
        print(f"Deleting item at row: {self.selected_row}")
        self.user_items.delete_expense(self.selected_row)
        print('dupa dupa dupa')
        self.user_items_list = self.user_items.get_expenses()
        print(self.user_items_list)
        self.show_user_items()
        self.info_panel.pack_forget()
        self.app.update_user_expenses(self.user_items)

    def show_photo(self):
        print(self.row_id)
        print(self.user_items.get_expense(self.selected_row)[6])
        file_path = self.user_items.get_expense(self.selected_row)[6]
        print('dupsko')

        if file_path and os.path.exists(file_path):
            photo_dialog = CTkToplevel(self)
            photo_dialog.title("Expense Photo")

            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)
            photo_label = CTkLabel(photo_dialog, image=photo)
            photo_label.image = photo
            photo_label.pack(expand=True, fill='both', padx=20, pady=20)
        else:
            messagebox.showinfo("No photo", "No photo found for this expense")

    def get_filtered_expenses(self):
        date = self.date_filter.get()
        category = self.category_filter.get()
        sort = self.sort_filter.get()

        self.user_items_list = self.controller.get_filtered_expenses(date, category, sort)
        self.get_filtered_items()

    def upload_photo(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("Image Files", "*.jpeg"),
                       ("Image Files", "*.bmp")])
        if file_path:
            self.recipe_entry = file_path

    def save_edited_expense(self):
        new_expense = Expense(amount=self.amount_entry.get(),
                              category=self.category_entry.get(),
                              date=self.date_entry.get(),
                              payment_method=self.payment_method_entry.get(),
                              )

        self.user_items.update_user_expense(self.selected_row, new_expense)
        self.user_items_list = self.user_items.get_expenses()
        self.show_user_expenses()
        self.edit_dialog.destroy()



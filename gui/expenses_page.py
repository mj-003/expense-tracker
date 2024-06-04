from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image, ImageTk
from customtkinter import *

from categories import Categories
from financials.expense import Expense
from item_page_abc import FinancialsPage
from widgets_and_buttons import *


class ExpensesPage(FinancialsPage):
    def __init__(self, parent, app, user_expenses):
        super().__init__(parent=parent, app=app, user_items=user_expenses, user_items2=None)

        self.title = 'Expenses'

        # Filters
        self.sort_filter = None
        self.category_filter = None
        self.date_filter = None

        # Entry fields
        self.amount_entry = None
        self.category_entry = None
        self.date_entry = None
        self.payment_method_entry = None
        self.recipe_entry = None

        # User data
        self.user_items = user_expenses
        self.user_items_list = user_expenses.get_expenses()

        # Create the page
        self.create_title_frame()
        self.create_metrics_frame(self.show_add_expense_form)
        self.create_search_container_expense()
        self.create_info_panel()
        self.show_user_expenses()

    def show_user_expenses(self):
        """
        Shows the user's expenses
        :return:
        """
        self.user_items_list = self.user_items.get_expenses()
        self.show_user_items()

    def create_search_container_expense(self):
        """
        Creates the search container for the expenses page
        :return:
        """
        # Create the search container from the abstract class
        self.create_search_container(self.get_more_expense_info)

        # Create the rest of the search container
        self.category_filter = get_categories_combo_box(self.search_container, 155)
        self.category_filter.pack(side="left", padx=(13, 0), pady=15)

        self.sort_filter = get_sort_combo_box(self.search_container, 155)
        self.sort_filter.pack(side="left", padx=(13, 0), pady=15)

        check_button2 = get_check_button(self.search_container, self.get_filtered_expenses)
        check_button2.pack(side="left", padx=(13, 0), pady=15)

    def get_more_expense_info(self):
        """
        Gets more info about an expense
        :return:
        """
        # Get the row id
        if (not self.row_id.get().isdigit()) or int(self.row_id.get()) < 1 or int(self.row_id.get()) > len(
                self.user_items.get_expenses()):
            messagebox.showwarning("Warning", "Invalid ID.")
            return
        else:
            self.selected_row = int(self.row_id.get())
            self.item_info = self.user_items.get_expenses()[self.selected_row]
            self.get_more_info()

        photo_button = CTkButton(self.info_panel, text="Recipe", fg_color='#2A8C55', text_color='white',
                                 command=lambda: self.show_photo())
        photo_button.pack(padx=15, pady=10, fill='both')

    def show_add_expense_form(self):
        """
        Shows the form to add a new expense
        :return:
        """
        # Call the method from the abstract class
        self.show_add_item_form()

        # Create the form
        self.amount_entry = CTkEntry(self.info_panel, placeholder_text="Price", validate='key',
                                     validatecommand=self.vcmd_money)
        self.amount_entry.pack(pady=(10, 10), padx=(10, 10))

        self.category_entry = get_categories_combo_box(self.info_panel, 145)
        self.category_entry.pack(pady=(10, 10), padx=(10, 10))

        self.add_date_entry(self.info_panel)

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

        self.add_buttons()
        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def validate_and_save(self):
        """
        Validates the form and saves the new expense
        :return:
        """
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        payment = self.payment_method_entry.get()
        date = self.date_entry.get()

        if not amount or not category or not payment or not date:
            messagebox.showwarning("Warning", "Please fill in all fields.")
        else:
            self.save_new_item()

    def save_new_item(self):
        """
        Saves the new expense
        :return:
        """
        new_price = self.amount_entry.get()
        new_category = self.category_entry.get()
        new_date = self.date_entry.get()
        new_payment = self.payment_method_entry.get()

        # Create the new expense
        path = self.recipe_entry if self.recipe_entry else None
        self.new_item = Expense(amount=new_price, category=new_category, payment_method=new_payment, date=new_date,
                                photo_path=path)

        # Clear the form
        self.cancel()

        # Add the new expense
        self.user_items.add_expense(self.new_item)
        self.user_items_list = self.user_items.get_expenses()
        self.show_user_items()

    def edit_item(self):
        """
        Opens a dialog to edit an expense
        :return:
        """
        self.edit_dialog = ctk.CTkToplevel(self)
        self.edit_dialog.title(f"Edit {self.title}")
        self.edit_dialog.geometry("330x300")

        # Get the row id
        self.item_info = self.user_items.get_expenses()[self.selected_row]

        CTkLabel(self.edit_dialog, text="Price:").grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.amount_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[1]), validate='key',
                                     validatecommand=self.vcmd_money)
        self.amount_entry.grid(row=1, column=1, pady=(20, 10), padx=10, sticky="w")

        CTkLabel(self.edit_dialog, text="Category:").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.category_entry = get_categories_combo_box(self.edit_dialog, 140)
        self.category_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        CTkLabel(self.edit_dialog, text="Date:").grid(row=3, column=0, pady=10, padx=10, sticky="e")

        # from abstract class
        self.add_date_entry(self.edit_dialog, my_row=3, my_column=1, my_pady=10, my_padx=10, my_sticky="w")

        CTkLabel(self.edit_dialog, text="Payment method:").grid(row=4, column=0, pady=10, padx=10, sticky="e")
        self.payment_method_entry = CTkComboBox(self.edit_dialog, values=['Online', 'Card', 'Cash', 'Other'])
        self.payment_method_entry.grid(row=4, column=1, pady=10, padx=10, sticky='w')

        save_button = ctk.CTkButton(self.edit_dialog, text="Save", fg_color="#2A8C55", command=lambda: self.save_edited_expense())
        save_button.grid(row=5, column=0, columnspan=2, pady=20, padx=20, sticky='w')

        cancel_button = ctk.CTkButton(self.edit_dialog, text="Cancel", fg_color="#2A8C55", command=lambda: self.go_back())
        cancel_button.grid(row=5, column=1, columnspan=2, pady=20, padx=20, sticky='e')

        self.edit_dialog.columnconfigure(0, weight=1)
        self.edit_dialog.columnconfigure(1, weight=3)

    def delete_item(self):
        """
        Deletes an expense
        :return:
        """
        self.user_items.delete_expense(self.selected_row)
        self.user_items_list = self.user_items.get_expenses()
        self.show_user_items()
        self.info_panel.pack_forget()

    def show_photo(self):
        """
        Shows the photo of the expense
        :return:
        """
        file_path = self.user_items.get_expense(self.selected_row)[6]

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
        """
        Filters the expenses
        :return:
        """
        date = self.date_filter.get()
        category = self.category_filter.get()
        sort = self.sort_filter.get()

        # Get the filtered expenses from the controller
        self.user_items_list = self.controller.get_filtered_expenses(date_filter=date, category_filter=category, sort_order=sort)
        self.get_filtered_items()

    def upload_photo(self):
        """
        Uploads a photo of the expense
        :return:
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("Image Files", "*.jpeg"),
                       ("Image Files", "*.bmp")])
        if file_path:
            self.recipe_entry = file_path

    def save_edited_expense(self):
        """
        Saves the edited expense
        :return:
        """
        new_expense = Expense(amount=self.amount_entry.get(),
                              category=self.category_entry.get(),
                              date=self.date_entry.get(),
                              payment_method=self.payment_method_entry.get(),
                              )

        self.user_items.update_user_expense(self.selected_row, new_expense)
        self.user_items_list = self.user_items.get_expenses()
        self.show_user_expenses()
        self.edit_dialog.destroy()

    def cancel(self):
        """
        Clears the form
        :return:
        """
        self.amount_entry.delete(0, 'end')
        self.recipe_entry = None
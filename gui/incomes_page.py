from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

from financials.income import Income
from gui.item_page_abc import FinancialsPage
from gui.widgets_and_buttons import *


class IncomesPage(FinancialsPage):
    """

    Class IncomePage.
    Inherits from FinancialsPage.

    This class is responsible for creating the Incomes page.
    Users can add, edit, delete and view their incomes.
    User can also filter the incomes by date, sender and sort them.

    """
    def __init__(self, parent, app, user_incomes, currency):
        super().__init__(parent=parent, app=app, user_items=user_incomes, currency=currency)

        self.title = 'Incomes'

        # Filters
        self.sort_filter = None
        self.from_filter = None
        self.date_filter = None

        # Entry fields
        self.amount_entry = None
        self.from_entry = None
        self.date_entry = None

        # User data
        self.user_items = user_incomes
        self.user_items_list = user_incomes.get_incomes()

        # title
        self.new_title = f"Total incomes this month: {self.today_sum:.2f} zł"

        # Create the page
        self.create_title_frame()
        self.create_metrics_frame(self.show_add_income_form, new_title=self.new_title)
        self.create_search_container_income()
        self.create_info_panel()
        self.show_user_items()

    def create_search_container_income(self):
        """

        Creates the search container for the Incomes page.
        This container contains the filters for the incomes.

        The filters are:
        - Date
        - From
        - Sort

        """
        # Create the search container from the abstract class
        self.create_search_container(self.get_more_income_info)

        # Create the rest of the search container
        self.date_filter = get_date_combo_box(self.search_container, 155)
        self.date_filter.pack(side="left", padx=(13, 0), pady=15)

        self.from_filter = get_entry(self.search_container, 155, "From")
        self.from_filter.pack(side="left", padx=(13, 0), pady=15)

        self.sort_filter = get_sort_combo_box(self.search_container, 155)
        self.sort_filter.pack(side="left", padx=(13, 0), pady=15)

        check_button2 = get_check_button(self.search_container, self.get_filtered_incomes, 30)
        check_button2.pack(side="left", padx=(13, 0), pady=15)

    def get_more_income_info(self):
        """

        Validate an entered income id.
        And then (in validate_id, function get_more_info) get more information about the income.

        """
        self.validate_id(self.user_items.get_incomes())

    def show_add_income_form(self):
        """

        Show the form to add a new income.
        It includes:
        - Amount
        - From
        - Date
        - Description (optional)

        User can add new income, go back or cancel the form.

        """
        # Call the method from the abstract class
        self.show_add_item_form()

        # Create the form
        self.amount_entry = CTkEntry(self.info_panel, placeholder_text="Amount", validate='key',
                                     validatecommand=self.vcmd_money, border_width=1, border_color="#2A8C55")
        self.amount_entry.pack(pady=(15, 10), padx=(10, 10))

        self.from_entry = CTkEntry(self.info_panel, placeholder_text="From", border_width=1, border_color="#2A8C55")
        self.from_entry.pack(pady=(10, 10), padx=(10, 10))

        # Add rest from abstract class
        self.date_var = StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = CTkEntry(self.info_panel, textvariable=self.date_var, state='readonly', fg_color="white", border_width=1, border_color="#2A8C55")
        self.date_entry.pack(pady=(10, 10), padx=(10, 10))
        self.date_entry.bind("<Button-1>", self.open_calendar)

        CTkButton(master=self.info_panel,
                  text="Add Description",
                  fg_color="white",
                  hover_color="#207244",
                  font=("Aptos", 12),
                  border_color="#2A8C55",
                  border_width=1,
                  text_color="#2A8C55",
                  text_color_disabled="white",
                  command=self.add_description).pack(pady=(5, 5), padx=(10, 10))

        self.add_buttons()
        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def validate_and_save(self):
        """

        Validate the entered income and save it.

        Amount, From and Date are required fields.

        If the validation is successful, save the income.
        If the validation is not successful, show a warning.

        """
        amount = self.amount_entry.get()
        from_entry = self.from_entry.get()
        date = self.date_var.get()

        if not amount or not from_entry or not date:
            messagebox.showwarning("Warning", "Please fill in all fields.")
        else:
            self.save_new_item()

    def save_new_item(self):
        """

        Save the new income.

        """
        new_price = self.amount_entry.get()
        new_from = self.from_entry.get()
        new_date = self.date_entry.get()

        # Create the new income
        self.new_item = Income(amount=new_price, sender=new_from, date=new_date, description=self.description)

        # Clear the form
        self.cancel()

        # Add the new income
        self.user_items.add_income(self.new_item)
        self.user_items_list = self.user_items.get_incomes()
        self.show_user_items()

    def edit_item(self):
        """

        Opens the form to edit the selected income.
        The form includes:
        - Amount
        - From
        - Date

        """

        # Create a dialog
        self.edit_dialog = ctk.CTkToplevel(self)
        self.edit_dialog.title(f"Edit {self.title}")
        self.edit_dialog.geometry("330x300")
        self.item_info = self.user_items.get_incomes()[self.selected_row]

        # Create the form
        CTkLabel(self.edit_dialog, text="Amount:").grid(row=1, column=0, pady=(50, 10), padx=10, sticky="e")
        self.amount_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[1]), validate='key',
                                     validatecommand=self.vcmd_money)
        self.amount_entry.grid(row=1, column=1, pady=(50, 10), padx=12, sticky="w")

        CTkLabel(self.edit_dialog, text="From:").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.from_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[2]))
        self.from_entry.grid(row=2, column=1, pady=(20, 10), padx=12, sticky="w")

        CTkLabel(self.edit_dialog, text="Date:").grid(row=3, column=0, pady=10, padx=10, sticky="e")
        self.date_var = StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = CTkEntry(self.edit_dialog, textvariable=self.date_var, state='readonly', fg_color="white")
        self.date_entry.bind("<Button-1>", self.open_calendar)
        self.date_entry.grid(row=3, column=1, pady=10, padx=12, sticky="w")

        # Create buttons
        save_button = CTkButton(self.edit_dialog, text="Save", fg_color="#2A8C55", hover_color='#207244',
                                command=lambda: self.save_edited_income())
        save_button.grid(row=4, column=0, columnspan=2, pady=20, padx=20, sticky='w')

        cancel_button = CTkButton(self.edit_dialog, text="Cancel", fg_color="#2A8C55", hover_color='#207244', command=lambda: self.go_back())
        cancel_button.grid(row=4, column=1, columnspan=2, pady=20, padx=20, sticky='e')

        # Configure the dialog
        self.edit_dialog.columnconfigure(0, weight=1)
        self.edit_dialog.columnconfigure(1, weight=3)

    def delete_item(self):
        """

        Delete the selected income.

        """
        self.user_items.delete_income(self.selected_row)
        self.user_items_list = self.user_items.get_incomes()
        self.show_user_items()

        # Hide the info panel after deleting
        self.info_panel.pack_forget()

    def get_filtered_incomes(self):
        """

        Get the filtered incomes.
        Filter by date and from, sort by amount or date.

        """
        date = self.date_filter.get()
        from_who = self.from_filter.get()
        sort = self.sort_filter.get()

        # Get the filtered incomes from the controller
        self.user_items_list = self.user_items.get_incomes(date, from_who, sort)
        self.get_filtered_items()

    def save_edited_income(self):
        """

        Save the edited income.

        """
        new_income = Income(amount=self.amount_entry.get(),
                            sender=self.from_entry.get(),
                            date=self.date_entry.get())

        # Update the income and list
        self.user_items.update_user_income(self.selected_row, new_income)
        self.user_items_list = self.user_items.get_incomes()

        self.show_user_items()
        self.edit_dialog.destroy()

    def cancel(self):
        """

        Clear the form.

        """
        self.amount_entry.delete(0, 'end')
        self.from_entry.delete(0, 'end')
        self.description = None

    def get_description(self):
        """

        Get the description of the selected income.

        """
        # income[5] is the description
        return self.user_items.get_income(self.selected_row)[5]


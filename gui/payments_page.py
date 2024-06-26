from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

from financials.payment import Payment
from gui.item_page_abc import FinancialsPage
from gui.widgets_and_buttons import *


class PaymentsPage(FinancialsPage):
    """

    Class PaymentPage.

    This inherits from the abstract class FinancialsPage.

    This class is responsible for displaying the payments page.
    Users can add, edit, delete and view payments.
    They can also filter and sort the payments.

    """
    def __init__(self, parent, app, user_payments, currency):
        super().__init__(parent=parent, app=app, user_items=user_payments, currency=currency)

        self.title = 'Payments'

        # Filters
        self.sort_filter = None
        self.title_filter = None
        self.date_filter = None

        # Entry fields
        self.date_entry = None
        self.amount_entry = None
        self.title_entry = None
        self.how_often_entry = None

        # User data
        self.user_items = user_payments
        self.user_items_list = user_payments.get_payments()

        # title
        self.new_title = f"Upcoming payments (in 3 days): {self.today_sum:.2f} zł"

        # Create the page
        self.create_title_frame()
        self.create_metrics_frame(self.show_add_payment_form, self.new_title)
        self.create_search_container_payment()
        self.create_info_panel()
        self.show_user_items()

    def create_search_container_payment(self):
        """

        Creates the search container for the payments page.
        It includes:
        - a date filter
        - a title filter
        - a sort filter
        - a check button to filter the payments

        (rest of the method is in the abstract class)

        """
        # Create the search container from the abstract class
        self.create_search_container(self.get_more_payment_info)

        # Create the rest of the search container
        self.date_filter = get_upcoming_combo_box(self.search_container, 155)
        self.date_filter.pack(side="left", padx=(13, 0), pady=15)

        self.title_filter = get_entry(self.search_container, 155, "Title")
        self.title_filter.pack(side="left", padx=(13, 0), pady=15)

        self.sort_filter = get_sort_combo_box(self.search_container, 155)
        self.sort_filter.pack(side="left", padx=(13, 0), pady=15)

        check_button2 = get_check_button(self.search_container, self.get_filtered_payments, my_width=30)
        check_button2.pack(side="left", padx=(13, 0), pady=15)

    def get_more_payment_info(self):
        """

        Validates the id of the payment and if it is valid, it shows the payment details.

        (rest of the method is in the abstract class)

        """
        self.validate_id(self.user_items.get_payments())

    def show_add_payment_form(self):
        """

        Shows the form to add a new payment.

        Add payment form includes:
        - title entry
        - amount entry
        - date entry
        - how often entry (combo box)
        - description

        """
        # Call the method from the abstract class
        self.show_add_item_form()

        # Create the form
        self.title_entry = CTkEntry(self.info_panel, placeholder_text="Title")
        self.title_entry.pack(pady=(10, 10), padx=(10, 10))

        self.amount_entry = CTkEntry(self.info_panel, placeholder_text="Amount", validate='key',
                                     validatecommand=self.vcmd_money)
        self.amount_entry.pack(pady=(10, 10), padx=(10, 10))

        self.date_var = StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = CTkEntry(self.info_panel, textvariable=self.date_var, state='readonly', fg_color="white")
        self.date_entry.pack(pady=(10, 10), padx=(10, 10))
        self.date_entry.bind("<Button-1>", self.open_calendar)

        self.how_often_entry = get_how_often_combo_box(self.info_panel, 145)
        self.how_often_entry.pack(pady=(10, 10), padx=(10, 10))

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

        # add buttons from the abstract class
        self.add_buttons()
        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def validate_and_save(self):
        """

        Validates the form and saves the new payment.
        Amount, how often, title and date are required.

        If the form is not filled in, a warning is shown.

        """
        amount = self.amount_entry.get()
        how_often = self.how_often_entry.get()
        title = self.title_entry.get()
        date = self.date_entry.get()

        if not amount or not how_often or not title or not date:
            messagebox.showwarning("Warning", "Please fill in all fields.")
        else:
            self.save_new_item()

    def save_new_item(self):
        """

        Saves the new payment and clears the form.

        """
        new_amount = self.amount_entry.get()
        new_how_often = self.how_often_entry.get()
        new_title = self.title_entry.get()
        new_date = self.date_entry.get()

        # Create the new payment
        self.new_item = Payment(amount=new_amount, title=new_title, date=new_date, how_often=new_how_often, description=self.description)

        # Clear the form
        self.cancel()

        # Add the new payment
        self.user_items.add_payment(self.new_item)
        self.user_items_list = self.user_items.get_payments()
        self.show_user_items()

    def edit_item(self):
        """

        Edit selected payment.
        The user can edit the title, amount, how often and date.

        """
        self.edit_dialog = ctk.CTkToplevel(self)
        self.edit_dialog.title(f"Edit {self.title}")
        self.edit_dialog.geometry("330x300")

        # Get the row id
        self.item_info = self.user_items.get_payments()[self.selected_row]

        CTkLabel(self.edit_dialog, text="Title:").grid(row=4, column=0, pady=10, padx=10, sticky="e")
        self.title_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[2]))
        self.title_entry.grid(row=1, column=1, pady=(20, 10), padx=10, sticky='w')

        CTkLabel(self.edit_dialog, text="Amount:").grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.amount_entry = CTkEntry(self.edit_dialog, textvariable=StringVar(value=self.item_info[1]), validate='key',
                                     validatecommand=self.vcmd_money)
        self.amount_entry.grid(row=2, column=1, pady=(10, 10), padx=10, sticky="w")

        CTkLabel(self.edit_dialog, text="How often:").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.how_often_entry = get_how_often_combo_box(self.edit_dialog, 140)
        self.how_often_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        CTkLabel(self.edit_dialog, text="Date:").grid(row=4, column=0, pady=10, padx=10, sticky="e")

        # from abstract class
        self.date_var = StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = CTkEntry(self.edit_dialog, textvariable=self.date_var, state='readonly', fg_color="white")
        self.date_entry.grid(row=4, column=1, pady=10, padx=10, sticky='w')
        self.date_entry.bind("<Button-1>", self.open_calendar)


        save_button = ctk.CTkButton(self.edit_dialog, text="Save", fg_color="#2A8C55", hover_color='#207244',
                                    command=lambda: self.save_edited_payment())
        save_button.grid(row=5, column=0, columnspan=2, pady=20, padx=20, sticky='w')

        cancel_button = ctk.CTkButton(self.edit_dialog, text="Cancel", fg_color="#2A8C55", hover_color='#207244',
                                      command=lambda: self.go_back())
        cancel_button.grid(row=5, column=1, columnspan=2, pady=20, padx=20, sticky='e')

        self.edit_dialog.columnconfigure(0, weight=1)
        self.edit_dialog.columnconfigure(1, weight=3)

    def delete_item(self):
        """

        Deletes the selected payment, based on the row id.
        Uptades the list of payments and shows the updated list.

        """
        self.user_items.delete_payment(self.selected_row)
        self.user_items_list = self.user_items.get_payments()
        self.show_user_items()
        self.info_panel.pack_forget()

    def get_filtered_payments(self):
        """

        Filters the payments based on the date, title and sort.

        """
        date = self.date_filter.get()
        title = self.title_filter.get()
        sort = self.sort_filter.get()

        # Get the filtered incomes from the controller
        self.user_items_list = self.user_items.get_payments(date, title, sort)
        self.get_filtered_items()

    def save_edited_payment(self):
        """

        Saves the edited payment.

        """
        new_payment = Payment(amount=self.amount_entry.get(),
                              title=self.title_entry.get(),
                              date=self.date_entry.get(),
                              how_often=self.how_often_entry.get())

        self.user_items.update_user_payments(self.selected_row, new_payment)
        self.user_items_list = self.user_items.get_payments()
        self.show_user_items()
        self.edit_dialog.destroy()

    def cancel(self):
        """

        Clears the form.

        """
        self.amount_entry.delete(0, 'end')
        self.title_entry.delete(0, 'end')
        self.description = None

    def get_description(self):
        """

        Gets the description of the selected payment.

        """
        # payment[6] is the description
        return self.user_items.get_payment(self.selected_row)[6]




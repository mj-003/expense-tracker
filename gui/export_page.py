from datetime import datetime

from gui.items_controller import ItemsController
from utils.exports import export_to_excel, export_to_csv
from gui.widgets_and_buttons import *


class ExportPage(CTkFrame):
    """

    Class ExportPage.
    This page allows the user to export their financial data to an Excel or CSV file.
    User can choose to export all data or filter the data by date and sort order.
    User can also choose to export only expenses, only incomes or both.

    """
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent)

        # Initialize the app, parent, user, and database
        self.app = app
        self.parent = parent
        self.user = user
        self.database = database

        # Initialize the filters and table
        self.item_filter = None
        self.date_filter = None
        self.table = None
        self.table_frame = None

        # Initialize the user expenses and incomes
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes

        # Initialize the user expenses and incomes lists
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.user_incomes_list = self.user_incomes.get_incomes()

        # Initialize the item controller and items list
        self.controller = ItemsController(user_expenses, user_incomes, self.user.currency)
        self.items_list = self.controller.create_user_items_list()

        # Create the widgets
        self.add_title()
        self.add_filters()
        self.add_table()

    def add_title(self):
        """

        Add the title and export button.

        """
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(fill="both", padx=27, pady=(25, 0))

        title = CTkLabel(master=title_frame, text="Export Financials", font=("Aptos", 40, 'bold'), text_color="#2A8C55")
        title.pack(anchor="nw", side="left")

        export_button = (CTkButton(master=title_frame, text="Export", width=100, height=50, font=("Aptos", 16), text_color="#fff", fg_color="#2A8C55", hover_color="#207244", corner_radius=50, command=self.export_data))
        export_button.pack(anchor="ne",side="right")

    def add_filters(self):
        """

        Add the filters.

        Filter include:
        - Date filter ('This month', 'This year', 'All')
        - Item filter ('Expenses', 'Incomes', 'Both')
        - Sort filter - ascending or descending for amount or date

        """
        self.filter_frame = CTkFrame(master=self, fg_color="transparent")
        self.filter_frame.pack(fill="both", padx=27, pady=(31, 0))

        self.date_filter = get_date_combo_box(my_master=self.filter_frame, my_width=220)
        self.date_filter.grid(row=0, column=1, sticky="w", padx=(0, 20))

        self.item_filter = get_items_combo_box(my_master=self.filter_frame, my_width=220)
        self.item_filter.grid(row=0, column=2, sticky="w", padx=(0, 20))

        self.sort_filter = get_sort_combo_box(my_master=self.filter_frame, my_width=220)
        self.sort_filter.grid(row=0, column=4, sticky="w", padx=(0, 20))

        check_button = get_check_button(my_master=self.filter_frame, on_command=self.get_filtered_items, my_width=35)
        check_button.grid(column=5, sticky="e", padx=(0, 27), row=0)

    def add_table(self):
        """

        Add the table.

        """
        self.table_frame = CTkScrollableFrame(master=self, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        self.table = CTkTable(master=self.table_frame,
                              values=self.items_list,
                              colors=["#E6E6E6", "#EEEEEE"],
                              header_color="#2A8C55",
                              hover_color="#B4B4B4")

        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True, fill='both')

    def export_data(self):
        """

        Export the selected data to an Excel or CSV file.

        """
        current_date = datetime.now().strftime('%Y-%m-%d')
        default_filename = f"{self.user.username}_{current_date}"

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"),
                                                            ("CSV files", "*.csv")],
                                                 initialfile=default_filename)

        # Export the data
        if file_path:
            if self.item_filter.get() == 'Both':
                data = self.items_list
            elif self.item_filter.get() == 'Expenses':
                data = self.user_expenses.get_expenses(date_filter=self.date_filter.get(), sort_order=self.sort_filter.get())
            else:
                data = self.user_incomes.get_incomes(date_filter=self.date_filter.get(), sort_order=self.sort_filter.get())
            if file_path.endswith('.xlsx'):
                export_to_excel(file_path, data)
            elif file_path.endswith('.csv'):
                export_to_csv(file_path, data)

    def get_filtered_items(self):
        """

        Get the filtered items.
        If the user selects a filter, the items list will be updated accordingly.

        """
        self.items_list = self.controller.create_user_items_list()

        date = self.date_filter.get()
        item = self.item_filter.get()
        sort = self.sort_filter.get()

        self.items_list = self.controller.get_filtered_items(items_list=self.items_list, date=date, category=item, sort=sort)

        # Clear the table
        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        # Add the new rows
        for row_data in self.items_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")


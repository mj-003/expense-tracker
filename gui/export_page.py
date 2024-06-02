from datetime import datetime

from CTkTable import CTkTable
from customtkinter import *

from categories import Categories
from utils.exports import export_to_excel, export_to_csv
from export_page_controller import ExpensePageController
from item_controller import ItemController


class ExportPage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent)

        self.item_filter = None
        self.date_filter = None
        self.table = None
        self.table_frame = None
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes

        self.app = app
        self.parent = parent
        self.user = user
        self.database = database
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.user_incomes_list = self.user_incomes.get_incomes()
        self.controller = ItemController(database, user, user_expenses, user_incomes)
        self.items_list = self.controller.create_user_items_list()

        self.add_title()
        self.add_filters()
        self.add_table()

    def add_title(self):
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(fill="both", padx=27, pady=(25, 0))

        CTkLabel(master=title_frame,
                 text="Export Financials",
                 font=("Aptos", 40, 'bold'),
                 text_color="#2A8C55").pack(
            anchor="nw",
            side="left")

        CTkButton(master=title_frame,
                  text="Export",
                  width=100,
                  height=50,
                  font=("Aptos", 16),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  corner_radius=50,
                  command=self.export_data).pack(
            anchor="ne",
            side="right")

    def add_filters(self):
        self.filter_frame = CTkFrame(master=self, fg_color="transparent")
        self.filter_frame.pack(fill="both", padx=27, pady=(31, 0))

        self.date_filter = CTkComboBox(master=self.filter_frame,
                                       width=220,
                                       values=["Date", "This month", "This year"],
                                       button_color="#2A8C55",
                                       border_color="#2A8C55",
                                       border_width=2,
                                       button_hover_color="#207244",
                                       dropdown_hover_color="#207244",
                                       dropdown_fg_color="#2A8C55",
                                       dropdown_text_color="#fff")
        self.date_filter.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 20))

        self.item_filter = CTkComboBox(master=self.filter_frame,
                                       width=220,
                                       values=['Both', 'Expenses', 'Incomes'],
                                       button_color="#2A8C55",
                                       border_color="#2A8C55",
                                       border_width=2,
                                       button_hover_color="#207244",
                                       dropdown_hover_color="#207244",
                                       dropdown_fg_color="#2A8C55",
                                       dropdown_text_color="#fff")
        self.item_filter.grid(
            row=0,
            column=2,
            sticky="w",
            padx=(0, 20))

        self.sort_filter = CTkComboBox(master=self.filter_frame,
                                       width=220,
                                       values=['Sort', '⬆ Amount', '⬇ Amount', '⬆ Time', '⬇ Time'],
                                       button_color="#2A8C55",
                                       border_color="#2A8C55",
                                       border_width=2,
                                       button_hover_color="#207244",
                                       dropdown_hover_color="#207244",
                                       dropdown_fg_color="#2A8C55",
                                       dropdown_text_color="#fff")
        self.sort_filter.grid(
            row=0,
            column=4,
            sticky="w",
            padx=(0, 20))

        CTkButton(master=self.filter_frame,
                  text="✔",
                  width=35,
                  font=("Arial", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_filtered_items).grid(
            column=5,
            sticky="e",
            padx=(0, 27),
            row=0)

    def add_table(self):
        self.table_frame = CTkScrollableFrame(master=self, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        #self.items_list = self.select_items()

        self.table = CTkTable(master=self.table_frame,
                              values=self.items_list,
                              colors=["#E6E6E6", "#EEEEEE"],
                              header_color="#2A8C55",
                              hover_color="#B4B4B4")

        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True, fill='both')

    def export_data(self):

        current_date = datetime.now().strftime('%Y-%m-%d')
        default_filename = f"{self.user.username}_{current_date}"

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"),
                                                            ("CSV files", "*.csv")],
                                                 initialfile=default_filename)

        if file_path:
            if file_path.endswith('.xlsx'):
                export_to_excel(file_path, self.items_list)
            elif file_path.endswith('.csv'):
                export_to_csv(file_path, self.items_list)

    def get_filtered_items(self):
        self.items_list = self.controller.create_user_items_list()

        date = self.date_filter.get()
        item = self.item_filter.get()
        sort = self.sort_filter.get()

        self.items_list = self.controller.get_filtered_items(items_list=self.items_list, date=date, category=item, sort=sort)

        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        for row_data in self.items_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")


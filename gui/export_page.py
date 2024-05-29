from datetime import datetime

from CTkTable import CTkTable
from customtkinter import *

from categories import Categories
from utils.exports import export_to_excel, export_to_csv
from export_page_controller import ExpensePageController


class ExportPage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses):
        super().__init__(parent)

        self.category_filter = None
        self.date_filter = None
        self.table = None
        self.table_frame = None
        self.user_expenses = None

        self.app = app
        self.parent = parent
        self.user = user
        self.database = database
        self.user_expenses = user_expenses
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.controller = ExpensePageController(database, user, user_expenses)

        self.add_title()
        self.add_filters()
        self.add_table()

    def add_title(self):
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(fill="both", padx=27, pady=(15, 0))

        CTkLabel(master=title_frame,
                 text="Export Expenses",
                 font=("Arial Black", 25),
                 text_color="#2A8C55").pack(
            anchor="nw",
            side="left")

        CTkButton(master=title_frame,
                  text="EXPORT",
                  width=150,
                  font=("Arial", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.export_data).pack(
            anchor="ne",
            side="right",
            pady=(10, 0),
            padx=(0, 27))

        # CTkButton(master=title_frame,
        #           text="✔",
        #           width=35,
        #           font=("Arial", 15),
        #           text_color="#fff",
        #           fg_color="#2A8C55",
        #           hover_color="#207244",
        #           command=self.get_filtered_expenses).pack(
        #     anchor="ne",
        #     side="right",
        #     pady=(10, 0),
        #     padx=(0, 15))

    def add_filters(self):
        self.filter_frame = CTkFrame(master=self, fg_color="transparent")
        self.filter_frame.pack(fill="both", padx=27, pady=(31, 0))

        # add start date
        CTkLabel(master=self.filter_frame,
                 text="Filter:",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=0,
            column=0,
            sticky="w")

        self.date_filter = CTkComboBox(master=self.filter_frame,
                                       width=125,
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
            padx=(5, 15))

        # CTkLabel(master=self.filter_frame,
        #          text="Category:",
        #          font=("Arial Bold", 17),
        #          text_color="#52A476",
        #          justify="left").grid(
        #     row=0,
        #     column=2,
        #     sticky="w",
        #     padx=(20, 0))

        self.category_filter = CTkComboBox(master=self.filter_frame,
                                           width=125,
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
        self.category_filter.grid(
            row=0,
            column=2,
            sticky="w",
            padx=(5, 0))

        CTkLabel(master=self.filter_frame,
                 text="Sort:",
                 font=("Arial Bold", 17),
                 text_color="#52A476",
                 justify="left").grid(
            row=0,
            column=3,
            sticky="w",
            padx=(30, 5))

        self.sort_filter = CTkComboBox(master=self.filter_frame,
                                       width=125,
                                       values=['Sort','⬆ Amount', '⬇ Amount', '⬆ Time', '⬇ Time'],
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
            padx=(5, 0))

        CTkButton(master=self.filter_frame,
                  text="✔",
                  width=35,
                  font=("Arial", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_filtered_expenses).grid(
            column=5,
            sticky="e",
            padx=(35, 27),
            row=0)

    def add_table(self):
        self.table_frame = CTkScrollableFrame(master=self, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        self.table = CTkTable(master=self.table_frame,
                              values=self.user_expenses_list,
                              colors=["#E6E6E6", "#EEEEEE"],
                              header_color="#2A8C55",
                              hover_color="#B4B4B4")

        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True)

    def export_data(self):

        current_date = datetime.now().strftime('%Y-%m-%d')
        default_filename = f"{self.user.username}_{current_date}"

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"),
                                                            ("CSV files", "*.csv")],
                                                 initialfile=default_filename)

        if file_path:
            if file_path.endswith('.xlsx'):
                export_to_excel(file_path, self.user_expenses_list)
            elif file_path.endswith('.csv'):
                export_to_csv(file_path, self.user_expenses_list)

    def get_filtered_expenses(self):
        date = self.date_filter.get()
        category = self.category_filter.get()
        sort = self.sort_filter.get()

        self.user_expenses_list = self.controller.get_filtered_expenses(date, category, sort)

        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        for row_data in self.user_expenses_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")




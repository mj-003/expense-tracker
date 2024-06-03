import datetime

import customtkinter as ctk
from CTkTable import CTkTable
from PIL import Image
from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from item_controller import ItemController
from plots import MyPlotter
from datetime import datetime


class HomePage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent)
        self.current_month = datetime.now().replace(day=1)
        self.financials = None
        self.selected_row = None
        self.table_frame = None
        self.expense_id = None
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        self.app = app
        self.parent = parent
        self.user = user
        self.database = database
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.user_incomes_list = self.user_incomes.get_incomes()
        self.controller = ItemController(database, user, user_expenses, user_incomes)
        self.user_items_list = self.controller.create_user_items_list()

        self.plotter = MyPlotter(user_expenses, user_incomes)

        self.date_filter = None
        self.category_filter = None
        self.sort_filter = None
        self.var_show_chart = ctk.StringVar(value="on")
        self.today = datetime.today().strftime('%a, %-d.%m')

        self.create_title_frame()
        self.create_metrics_frame()
        self.create_search_container()
        self.show_user_items()
        self.create_chart_panel()
        self.if_show_chart()

    def create_title_frame(self):
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(
            anchor="n",
            fill="x",
            padx=27,
            pady=(25, 0))

        CTkLabel(master=title_frame,
                 text=f"Hello {self.user.username}!",
                 font=("Aptos", 40, 'bold'),
                 text_color="#2A8C55").pack(
            anchor="nw",
            side="left")

        CTkLabel(master=title_frame,
                 text=self.today,
                 text_color="#2A8C55",
                 font=("Aptos", 35)).pack(
            anchor='nw',
            side='right',
            pady=5)

    def create_metrics_frame(self):
        metrics_frame = CTkFrame(master=self, fg_color="transparent")
        metrics_frame.pack(
            anchor="n",
            fill="x",
            padx=27,
            pady=(27, 0))

        total_sum_metric = CTkFrame(master=metrics_frame,
                                    fg_color="#2A8C55",
                                    width=400,
                                    height=60,
                                    corner_radius=30)

        total_sum_metric.grid_propagate(False)
        total_sum_metric.pack(side="left")

        logistics_img_data = Image.open("images/money.png")
        logistics_img = CTkImage(light_image=logistics_img_data,
                                 dark_image=logistics_img_data,
                                 size=(43, 43))

        CTkLabel(master=total_sum_metric,
                 image=logistics_img,
                 text="").grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(12, 5),
            pady=10)

        CTkLabel(master=total_sum_metric,
                 text=f"Total balance this month: {self.user_incomes.get_sum()-self.user_expenses.get_sum():.2f} zł",
                 text_color="#fff",
                 font=("Aptos", 18)).grid(
            row=0,
            column=1,
            sticky="sw")

        date_frame = CTkFrame(master=metrics_frame,
                              fg_color="transparent",
                              width=200,
                              height=60)

        date_frame.grid_propagate(False)
        date_frame.pack(side="right")

    def create_search_container(self):
        search_container = CTkFrame(master=self,
                                    height=50,
                                    fg_color="#F0F0F0")

        search_container.pack(fill="x",
                              pady=(27, 0),
                              padx=27)

        self.date_filter = CTkComboBox(master=search_container,
                                       width=185,
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

        self.category_filter = CTkComboBox(master=search_container,
                                           width=185,
                                           values=['Both', 'Incomes', 'Expenses'],
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

        self.sort_filter = CTkComboBox(master=search_container,
                                       width=185,
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

        CTkButton(master=search_container,
                  text='✔',
                  width=30,
                  font=("Aptos", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_filtered_items).pack(
            side="left",
            padx=(13, 0),
            pady=15)

        self.is_chart = CTkCheckBox(master=search_container, text="Chart", font=('Aptos', 15),
                                    variable=self.var_show_chart, onvalue="on", offvalue="off",
                                    command=self.if_show_chart, fg_color="#2A8C55", width=30, height=30)
        self.is_chart.pack(pady=20)

    def show_user_items(self):
        if self.table_frame is None:
            self.table_frame = CTkScrollableFrame(master=self, fg_color="transparent")
            self.table_frame.pack(expand=True, fill="both", padx=27, pady=21, side='left')

            self.table = CTkTable(master=self.table_frame,
                                  values=self.user_items_list,
                                  colors=["#E6E6E6", "#EEEEEE"],
                                  header_color="#2A8C55",
                                  hover_color="#B4B4B4")

            self.table.pack(expand=True, fill='both')

        # Aktualizacja istniejącej tabeli
        else:
            # Usuwanie wszystkich istniejących wierszy
            indicates_to_remove = list(range(len(self.table.values)))
            self.table.delete_rows(indicates_to_remove)

            # Dodawanie nowych wierszy z aktualizacją drugiej kolumny
            for row_data in self.user_items_list:
                if len(row_data) > 1:
                    row_data[1] = f"{row_data[1]} zł"
                self.table.add_row(row_data)

        # Edytowanie pierwszego wiersza (zakładam, że chcesz to zrobić po każdej aktualizacji)
        if self.table.rows > 0:
            self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_filtered_items(self):
        self.user_items_list = self.controller.create_user_items_list()
        date = self.date_filter.get()
        category = self.category_filter.get()
        sort = self.sort_filter.get()

        self.user_items_list = self.controller.get_filtered_items(self.user_items_list, date, category, sort)

        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        for row_data in self.user_items_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def if_show_chart(self):
        if self.var_show_chart.get() == "on":
            self.info_panel.pack(expand=True, fill="both", pady=27, padx=(0, 27))
        else:
            self.info_panel.pack_forget()

    def create_chart_panel(self):
        print('create chart panel')
        self.info_panel = ctk.CTkFrame(master=self, fg_color="white", border_width=2, border_color="#2A8C55",
                                       corner_radius=10, width=200)
        self.info_panel.pack_forget()
        self.update_chart()

    def update_chart(self):
        # Clear the previous chart if it exists
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        month_str, self.user_incomes_list, self.user_expenses_list = self.controller.get_chart_data(self.current_month)
        fig, ax = self.plotter.plot_incomes_expenses_per_month(month_str, self.user_incomes_list,
                                                               self.user_expenses_list)

        chart_canvas = FigureCanvasTkAgg(fig, master=self.info_panel)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        button_frame = ctk.CTkFrame(master=self.info_panel, fg_color="transparent")
        button_frame.pack(side='bottom', pady=10)

        prev_button = ctk.CTkButton(master=button_frame, text="Previous", fg_color='#2A8C55',
                                    command=self.show_prev_month)
        prev_button.pack(side='left', padx=5)

        next_button = ctk.CTkButton(master=button_frame, text="Next", fg_color='#2A8C55', command=self.show_next_month)
        next_button.pack(side='right', padx=5)

    def show_prev_month(self):
        self.current_month = self.current_month - datetime.timedelta(days=1)
        self.current_month = self.current_month.replace(day=1)
        self.update_chart()

    def show_next_month(self):
        next_month = self.current_month + datetime.timedelta(days=31)
        self.current_month = next_month.replace(day=1)
        self.update_chart()

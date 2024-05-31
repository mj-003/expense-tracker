import datetime
import os
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import numpy as np

import customtkinter as ctk
from CTkTable import CTkTable
from PIL import Image, ImageTk
from customtkinter import *

from categories import Categories
from financials.expense import Expense
from gui.add_expense import ExpensePage
from home_page_controller import HomePageController
from gui.add_income import IncomePage


def create_user_items_list(user_expenses, user_incomes):
    cat_names = ['No.', 'Amount', 'Category', 'Date']
    user_expenses_list = user_expenses.get_expenses()
    user_incomes_list = user_incomes.get_incomes()
    user_items_list = [cat_names]
    print('----------user expenses----------')
    print(user_expenses_list)

    for i, expense in enumerate(user_expenses_list[1:]):
        user_items_list.append([i + 1] + [expense[1]] + ['Expense'] + [expense[4]])
    for i, income in enumerate(user_incomes_list[1:]):
        user_items_list.append([len(user_items_list) + 1] + [income[1]] + ['Income'] + [income[3]])
    return user_items_list


class HomePage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent)
        self.financials = None
        self.selected_row = None
        self.table_frame = None
        self.expense_id = None
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        self.user_items_list = create_user_items_list(self.user_expenses, self.user_incomes)
        self.app = app
        self.parent = parent
        self.user = user
        self.database = database
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.user_incomes_list = self.user_incomes.get_incomes()
        self.controller = HomePageController(database, user, user_expenses)

        self.date_filter = None
        self.category_filter = None
        self.sort_filter = None

        self.create_title_frame()
        self.create_metrics_frame()
        self.create_search_container()
        self.show_user_items()
        self.chart_frame = CTkFrame(master=self, fg_color="transparent")
        self.chart_frame.pack(fill='both', expand=True, padx=27, pady=(21, 0))
        self.show_charts()


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
                 text="Thur, 30.05",
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
                                    width=350,
                                    height=60,
                                    corner_radius=30)

        total_sum_metric.grid_propagate(False)
        total_sum_metric.pack(side="left")

        logistics_img_data = Image.open("images/logistics_icon.png")
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
                 text="Total financials: 1929,99 zł",
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
                                       width=160,
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
                                           width=160,
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
                                       width=160,
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

    def show_user_items(self):
        if self.table_frame is None:

            self.table_frame = CTkScrollableFrame(master=self, fg_color="transparent")
            self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)

            # Tworzenie nowej tabeli
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

            # Dodawanie nowych wierszy
            for row_data in self.user_items_list:
                self.table.add_row(row_data)

            # Edytowanie pierwszego wiersza (zakładam, że chcesz to zrobić po każdej aktualizacji)
        if self.table.rows > 0:
            self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_filtered_items(self):
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

    def show_chart_window(self):
        chart_window = CTkFrame(master=self, fg_color="transparent")
        chart_window.pack(
            fill="both",
            padx=27,
            pady=(21, 0))

    def show_charts(self):
        dates, expense_values, income_values = self.get_last_30_days_data()

        fig, ax = plt.subplots(figsize=(10, 4))

        width = 0.4
        ax.bar(np.array(dates) - datetime.timedelta(days=0.2), expense_values, width=width, label='Expenses',
               color='red')
        ax.bar(np.array(dates) + datetime.timedelta(days=0.2), income_values, width=width, label='Incomes',
               color='green')

        ax.set_xlabel('Date')
        ax.set_ylabel('Amount')
        ax.set_title('Incomes and Expenses in the Last 30 Days')
        ax.legend()

        # Format the date labels
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: (datetime.date.fromordinal(int(x))).strftime('%b %d')))
        fig.autofmt_xdate()

        # Clear any previous canvas before adding new one
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def get_last_30_days_data(self):
        today = datetime.date.today()
        date_30_days_ago = today - datetime.timedelta(days=30)

        expenses = self.user_expenses.get_expenses()
        incomes = self.user_incomes.get_incomes()

        expense_data = {}
        income_data = {}

        for expense in expenses[1:]:
            date = datetime.datetime.strptime(expense[4], '%Y-%m-%d').date()
            if date_30_days_ago <= date <= today:
                if date not in expense_data:
                    expense_data[date] = 0
                expense_data[date] += float(expense[1])

        for income in incomes[1:]:
            print('hkjavnkbgb ', income[3])
            date = datetime.datetime.strptime(income[3], '%Y-%m-%d').date()
            if date_30_days_ago <= date <= today:
                if date not in income_data:
                    income_data[date] = 0
                income_data[date] += float(income[1])

        dates = [date_30_days_ago + datetime.timedelta(days=i) for i in range(31)]
        expense_values = [expense_data.get(date, 0) for date in dates]
        income_values = [income_data.get(date, 0) for date in dates]

        return dates, expense_values, income_values



import datetime
import tkinter.messagebox as messagebox

import customtkinter as ctk
from PIL import Image
from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.charts_page_controller import ChartPageController
from plots import MyPlotter


class ChartsPage(CTkFrame):
    def __init__(self, parent, app, user_expenses, user_incomes):
        super().__init__(parent)
        self.app = app
        self.parent = parent
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes

        self.user_expenses_list = self.user_expenses.get_expenses()
        self.user_incomes_list = self.user_incomes.get_incomes()

        self.plotter = MyPlotter(user_expenses, user_incomes)
        self.chart_controller = ChartPageController(self.plotter, self.user_expenses, self.user_incomes)

        self.curr_month = datetime.datetime.now().replace(day=1)
        self.curr_month_str = self.curr_month.strftime('%Y-%m')
        self.curr_year = self.curr_month.year

        self.current_chart_function = None
        self.button_frame = None

        self.create_widgets()

    def create_widgets(self):
        self.title_label = CTkLabel(self, text="Charts", font=("Aptos", 40, 'bold'), text_color="#2A8C55")
        self.title_label.pack(pady=20)

        self.thumbnail_frame = CTkFrame(self)
        self.thumbnail_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.chart_frame = CTkFrame(self)
        self.chart_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.chart_frame.pack_forget()
        self.create_chart_thumbnails()

    def create_chart_thumbnails(self):
        charts = [
            {"title": "Category Pie Chart", "image": "images/pie_chart.png",
             "function": self.plotter.plot_category_pie_chart},
            {"title": "Monthly Expenses and Incomes", "image": "images/bar_chart.png",
             "function": self.plotter.plot_expenses_incomes},
            {"title": "Monthly Expenses and Incomes trends", "image": "images/linear_chart.png",
             "function": self.plotter.plot_income_expense_trends},
            {"title": "Yearly Box Plot of Expenses and Incomes", "image": "images/box_chart.png",
             "function": self.plotter.plot_box_plot_expenses_incomes}
        ]

        row = 0
        column = 0

        for chart in charts:
            chart_image = Image.open(chart["image"])
            chart_image = chart_image.resize((150, 150))
            chart_image = CTkImage(light_image=chart_image, dark_image=chart_image, size=(150, 150))

            chart_button = CTkButton(self.thumbnail_frame, image=chart_image, text=chart["title"],
                                     font=('Aptos', 14, 'bold'), compound="top", fg_color='#2A8C55',
                                     command=lambda chart_func=chart["function"]: self.show_chart(chart_func,
                                                                                                  month=self.curr_month_str,
                                                                                                  year=self.curr_year))
            chart_button.grid(row=row, column=column, pady=20, padx=20, sticky="nsew")

            column += 1
            if column > 1:
                column = 0
                row += 1

        for i in range(2):
            self.thumbnail_frame.columnconfigure(i, weight=1)
        for i in range(row + 1):
            self.thumbnail_frame.rowconfigure(i, weight=1)

    def show_chart(self, chart_function, month, year):
        if self.button_frame:
            self.button_frame.destroy()

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        self.current_chart_function = chart_function
        self.switch_to_chart_frame()

        if self.chart_controller.check_available_data(chart_function, month, year):
            fig, ax = self.chart_controller.show_chart(chart_function, month, year)
            if fig and ax:
                chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
                chart_canvas.draw()
                chart_canvas.get_tk_widget().pack(fill='both', expand=True)
                self.add_buttons()
        else:
            self.switch_to_thumbnail_frame()
            messagebox.showinfo("No Data", "No data available for the selected period.")

    def switch_to_chart_frame(self):
        self.thumbnail_frame.pack_forget()
        self.title_label.pack_forget()
        self.chart_frame.pack(pady=(10, 10), padx=(10), fill='both', expand=True)
        self.button_frame = CTkFrame(master=self.chart_frame, height=50)
        self.button_frame.pack(side='bottom', pady=10, padx=10, fill='x')

    def switch_to_thumbnail_frame(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        self.curr_month = datetime.datetime.now().replace(day=1)
        self.curr_month_str = self.curr_month.strftime('%Y-%m')
        self.chart_frame.pack_forget()
        self.title_label.pack(pady=20)
        self.thumbnail_frame.pack(pady=10, padx=10, fill='both', expand=True)

    def add_buttons(self):
        back_button = CTkButton(self.button_frame, text="Back", fg_color='#2A8C55',
                                command=self.switch_to_thumbnail_frame)
        back_button.pack(side='left', padx=27, pady=15)

        next_button = ctk.CTkButton(master=self.button_frame, text="Next", fg_color='#2A8C55', command=self.show_next)
        next_button.pack(side='right', padx=(20, 27), pady=15)

        prev_button = ctk.CTkButton(master=self.button_frame, text="Previous", fg_color='#2A8C55',
                                    command=self.show_prev)
        prev_button.pack(side='right', padx=(0, 0), pady=15)

    def show_prev(self):
        prev_month, prev_year = self.chart_controller.show_prev_month()
        if self.current_chart_function:
            self.show_chart(self.current_chart_function, month=prev_month, year=prev_year)

    def show_next(self):
        next_month_str, next_year = self.chart_controller.show_next_month()
        if self.current_chart_function:
            self.show_chart(self.current_chart_function, month=next_month_str, year=next_year)


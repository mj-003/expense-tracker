import customtkinter as ctk
from PIL import Image
from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from plots import MyPlotter


class ChartsPage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent)
        self.user_expenses = user_expenses
        self.app = app
        self.parent = parent
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.create_widgets()
        self.plotter = MyPlotter(user_expenses)

    def create_widgets(self):
        self.title_label = CTkLabel(self, text="Charts", font=("Arial Black", 25), text_color="#2A8C55")
        self.title_label.pack(pady=20)

        self.thumbnail_frame = CTkFrame(self)
        self.thumbnail_frame.pack(pady=10, padx=10, fill='both', expand=True)

        self.chart_frame = CTkFrame(self)
        self.chart_frame.pack(pady=10, padx=10, fill='both', expand=True)
        self.chart_frame.pack_forget()  # Ukryj początkowo wykres

        self.create_chart_thumbnails()

    def create_chart_thumbnails(self):
        charts = [
            {"title": "Category Pie Chart", "image": "images/pie_chart.png", "function": self.show_category_pie_chart},
            {"title": "Monthly Expenses Bar Chart", "image": "images/delivered_icon.png", "function": self.show_monthly_expenses_bar_chart},
            {"title": "Expenses Over Time Line Chart", "image": "images/delivered_icon.png", "function": self.show_expenses_over_time_line_chart},
            {"title": "Comparison of Monthly Expenses", "image": "images/delivered_icon.png", "function": self.show_comparison_chart}
        ]

        row = 0
        column = 0
        for index, chart in enumerate(charts):
            chart_image = Image.open(chart["image"])
            chart_image = chart_image.resize((150, 150))  # Zmieniony rozmiar obrazu
            chart_image = CTkImage(light_image=chart_image, dark_image=chart_image, size=(150, 150))

            chart_button = CTkButton(self.thumbnail_frame, image=chart_image, text=chart["title"], compound="top", command=chart["function"])
            chart_button.grid(row=row, column=column, pady=20, padx=20, sticky="nsew")

            column += 1
            if column > 1:
                column = 0
                row += 1

        # Konfiguracja proporcji w siatce, aby wypełniała dostępną przestrzeń
        for i in range(2):  # 2 kolumny
            self.thumbnail_frame.columnconfigure(i, weight=1)
        for i in range(row + 1):  # liczba rzędów
            self.thumbnail_frame.rowconfigure(i, weight=1)

    def show_category_pie_chart(self):
        self.switch_to_chart_frame()
        fig, ax = self.plotter.plot_category_pie_chart()

        chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.add_back_button()
        self.add_prev_next_month_button()
        self.add_export_chart_button()

    def show_monthly_expenses_bar_chart(self):
        self.switch_to_chart_frame()
        fig, ax = self.plotter.plot_monthly_expenses_bar_chart()

        chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.add_back_button()
        self.add_prev_next_month_button()
        self.add_export_chart_button()

    def show_expenses_over_time_line_chart(self):
        self.switch_to_chart_frame()
        fig, ax = self.plotter.plot_expenses_over_time_line_chart()

        chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.add_back_button()
        self.add_prev_next_month_button()
        self.add_export_chart_button()

    def show_comparison_chart(self):
        self.switch_to_chart_frame()
        fig, ax = self.plotter.plot_comparison_chart()

        chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.add_back_button()
        self.add_prev_next_month_button()
        self.add_export_chart_button()

    def add_prev_next_month_button(self):
        pass

    def add_export_chart_button(self):
        pass
    def switch_to_chart_frame(self):
        self.thumbnail_frame.pack_forget()
        self.title_label.pack_forget()
        self.chart_frame.pack(pady=10, padx=10, fill='both', expand=True)

    def switch_to_thumbnail_frame(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        self.chart_frame.pack_forget()
        self.title_label.pack(pady=20)
        self.thumbnail_frame.pack(pady=10, padx=10, fill='both', expand=True)

    def add_back_button(self):
        back_button = CTkButton(self.chart_frame, text="Back to Thumbnails", command=self.switch_to_thumbnail_frame)
        back_button.pack(pady=10)

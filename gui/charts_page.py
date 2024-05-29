from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkToplevel, CTkImage
from PIL import Image

class ChartsPage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses):
        super().__init__(parent)
        self.user_expenses = user_expenses
        self.app = app
        self.parent = parent
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.create_widgets()

    def create_widgets(self):
        title_label = CTkLabel(self, text="Charts", font=("Arial Black", 25), text_color="#2A8C55")
        title_label.pack(pady=20)

        self.create_chart_thumbnails()

    def create_chart_thumbnails(self):
        thumbnail_frame = CTkFrame(self)
        thumbnail_frame.pack(pady=10, padx=10, fill='both', expand=True)

        charts = [
            {"title": "Category Pie Chart", "image": "images/delivered_icon.png", "function": self.show_category_pie_chart},
            {"title": "Monthly Expenses Bar Chart", "image": "images/delivered_icon.png", "function": self.show_monthly_expenses_bar_chart},
            {"title": "Expenses Over Time Line Chart", "image": "images/delivered_icon.png", "function": self.show_expenses_over_time_line_chart},
            {"title": "Comparison of Monthly Expenses", "image": "images/delivered_icon.png", "function": self.show_comparison_chart}
        ]

        row = 0
        column = 0
        for index, chart in enumerate(charts):
            chart_frame = CTkFrame(thumbnail_frame)
            chart_frame.grid(row=row, column=column, pady=10, padx=10, sticky="nsew")

            chart_image = Image.open(chart["image"])
            chart_image = chart_image.resize((100, 100))
            chart_image = CTkImage(light_image=chart_image, dark_image=chart_image, size=(100, 100))

            chart_label = CTkLabel(chart_frame, image=chart_image)
            chart_label.image = chart_image
            chart_label.pack(pady=5)

            chart_title = CTkLabel(chart_frame, text=chart["title"], font=("Arial", 15))
            chart_title.pack(pady=5, anchor='s')

            chart_button = CTkButton(chart_frame, text="View Chart", command=chart["function"])
            chart_button.pack(pady=5, anchor='s')

            column += 1
            if column > 1:
                column = 0
                row += 1

        # Konfiguracja proporcji w siatce, aby wypełniała dostępną przestrzeń
        for i in range(2):  # 2 kolumny
            thumbnail_frame.columnconfigure(i, weight=1)
        for i in range(2):  # 2 rzędy (lub więcej w zależności od liczby wykresów)
            thumbnail_frame.rowconfigure(i, weight=1)

    def show_category_pie_chart(self):
        categories = {}
        for expense in self.user_expenses_list[1:]:
            category = expense[2]
            amount = float(expense[1])
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

        labels = list(categories.keys())
        sizes = list(categories.values())

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        chart_window = CTkToplevel(self)
        chart_window.title("Category Pie Chart")
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

    def show_monthly_expenses_bar_chart(self):
        monthly_expenses = {}
        for expense in self.user_expenses_list[1:]:
            month = expense[4][:7]  # Assuming date format is YYYY-MM-DD
            amount = float(expense[1])
            if month in monthly_expenses:
                monthly_expenses[month] += amount
            else:
                monthly_expenses[month] = amount

        labels = list(monthly_expenses.keys())
        values = list(monthly_expenses.values())

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        plt.xticks(rotation=45)
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.title('Monthly Expenses')

        chart_window = CTkToplevel(self)
        chart_window.title("Monthly Expenses Bar Chart")
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

    def show_expenses_over_time_line_chart(self):
        dates = []
        amounts = []
        for expense in self.user_expenses_list[1:]:
            dates.append(expense[4])
            amounts.append(float(expense[1]))

        fig, ax = plt.subplots()
        ax.plot(dates, amounts, marker='o')
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Expenses Over Time')

        chart_window = CTkToplevel(self)
        chart_window.title("Expenses Over Time Line Chart")
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

    def show_comparison_chart(self):
        current_year = datetime.now().year
        last_year = current_year - 1
        current_year_expenses = {}
        last_year_expenses = {}

        for expense in self.user_expenses_list[1:]:
            year = int(expense[4][:4])
            month = expense[4][5:7]
            amount = float(expense[1])

            if year == current_year:
                if month in current_year_expenses:
                    current_year_expenses[month] += amount
                else:
                    current_year_expenses[month] = amount
            elif year == last_year:
                if month in last_year_expenses:
                    last_year_expenses[month] += amount
                else:
                    last_year_expenses[month] = amount

        months = list(current_year_expenses.keys())
        current_year_values = [current_year_expenses.get(month, 0) for month in months]
        last_year_values = [last_year_expenses.get(month, 0) for month in months]

        fig, ax = plt.subplots()
        ax.plot(months, current_year_values, marker='o', label=f'{current_year}')
        ax.plot(months, last_year_values, marker='o', label=f'{last_year}')
        plt.xticks(rotation=45)
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.title('Comparison of Monthly Expenses (This Year vs Last Year)')
        plt.legend()

        chart_window = CTkToplevel(self)
        chart_window.title("Comparison of Monthly Expenses (This Year vs Last Year)")
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

# Example usage of ChartsPage in an app

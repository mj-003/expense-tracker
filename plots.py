from datetime import datetime

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from financials.user_expenses import UserExpenses


class MyPlotter:
    def __init__(self, user_expenses: UserExpenses):
        self.user_expenses_list = user_expenses.get_expenses()[1:]
        self.amount_column = 1
        self.category_column = 2
        self.date_column = 4

    def plot_category_pie_chart(self):
        categories = {}
        for expense in self.user_expenses_list:
            category = expense[self.category_column]
            amount = float(expense[self.amount_column])
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

        labels = list(categories.keys())
        sizes = list(categories.values())

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        return fig, ax


    def plot_monthly_expenses_bar_chart(self):
        monthly_expenses = {}
        for expense in self.user_expenses_list:
            month = expense[self.date_column][:7]  # Assuming date format is YYYY-MM-DD
            amount = float(expense[self.amount_column])
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

        return fig, ax

    def plot_expenses_over_time_line_chart(self):
        dates = []
        amounts = []
        for expense in self.user_expenses_list:
            dates.append(expense[self.date_column])
            amounts.append(float(expense[self.amount_column]))

        fig, ax = plt.subplots()
        ax.plot(dates, amounts, marker='o')
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Expenses Over Time')

        return fig, ax



    def plot_comparison_chart(self):
        current_year = datetime.now().year
        last_year = current_year - 1
        current_year_expenses = {}
        last_year_expenses = {}

        for expense in self.user_expenses_list:
            year = int(expense[self.date_column][:4])
            month = expense[self.date_column][:7]
            amount = float(expense[self.amount_column])

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

        return fig, ax
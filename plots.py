from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates


from financials.user_expenses import UserExpenses
import pandas as pd

from financials.user_incomes import UserIncomes


class MyPlotter:
    def __init__(self, user_expenses: UserExpenses, user_incomes: UserIncomes):
        self.user_expenses_list = user_expenses.get_expenses()[1:]
        self.user_incomes_list = user_incomes.get_incomes()[1:]
        self.amount_column = 1
        self.category_column = 2
        self.date_column = 4

    def plot_category_pie_chart(self, month, year=None):
        colors = ['#5DADE2', '#AF7AC5', '#F1948A', '#F7DC6F', '#76D7C4', '#7FB3D5', '#A569BD']

        filtered_expenses = self.get_expenses_by_month(month)

        categories = {}
        for expense in filtered_expenses:
            category = expense[self.category_column]
            amount = float(expense[self.amount_column])
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

        labels = list(categories.keys())
        sizes = list(categories.values())

        fig, ax = plt.subplots()  # zmniejszenie rozmiaru wykresu

        # Wykres pierścieniowy
        wedges, texts, autotexts = ax.pie(sizes, colors=colors, autopct='%1.0f%%',
                                          shadow=False, startangle=140, wedgeprops=dict(width=0.5), pctdistance=0.85)

        centre_circle = plt.Circle((0, 0), 0.01, fc='white')
        fig.gca().add_artist(centre_circle)

        # Dodanie tekstu "Expense" w środku koła
        plt.text(0, 0, 'Expenses', ha='center', va='center', fontsize=12)

        # Upewnienie się, że wykres jest okrągły
        ax.axis('equal')

        for text in texts:
            text.set_text('')

        plt.subplots_adjust(right=0.7)
        plt.legend(wedges, labels, bbox_to_anchor=(1, 0.5), ncol=1, loc='center left', fontsize='small', frameon=False)
        plt.title(f'{month}', loc='right')


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

    def plot_incomes_expenses_per_month(self, month, incomes_list, expenses_list):

        incomes_pd = pd.DataFrame(incomes_list, columns=["ID", "Amount", "From", "Date"])
        expenses_pd = pd.DataFrame(expenses_list,
                                   columns=["ID", "Amount", "Category", "Payment method", "Date", "Photo path"])
        incomes_pd['Date'] = pd.to_datetime(incomes_pd['Date'])
        expenses_pd['Date'] = pd.to_datetime(expenses_pd['Date'])

        incomes_pd = incomes_pd[incomes_pd['Date'].dt.strftime('%Y-%m') == month]
        expenses_pd = expenses_pd[expenses_pd['Date'].dt.strftime('%Y-%m') == month]
        total_income = incomes_pd['Amount'].sum()
        total_expenses = expenses_pd['Amount'].sum()

        fig, ax = plt.subplots(figsize=(3, 2))

        # Set the background color to transparent
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        categories = ['Income', 'Expenses']
        amounts = [total_income, total_expenses]
        colors = ['#2A8C55', '#207244']

        # Plot the bars and add text
        bars = ax.bar(categories, amounts, color=colors, edgecolor='none')
        for i, amount in enumerate(amounts):
            ax.text(i, amount, f'{amount}', ha='center', va='bottom')

        # Remove the spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Set limits and labels
        ax.set_xlim(-0.5, len(categories) - 0.5)
        ax.set_ylim(0, max(amounts) * 1.1)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories)

        ax.set_title('Month: ' + month)

        return fig, ax

    def get_expenses_by_month(self, month):
        filtered_expenses = []
        for expense in self.user_expenses_list:
            if expense[self.date_column][:7] == month:
                filtered_expenses.append(expense)

        return filtered_expenses

    def plot_expenses_incomes(self, year, month=None):
        # Create DataFrames with the given data
        expense_df = pd.DataFrame(self.user_expenses_list, columns=['ID', 'Amount', 'Category', 'Payment','Date', 'Recipe'])
        income_df = pd.DataFrame(self.user_incomes_list, columns=['ID','Amount', 'From', 'Date'])

        expense_df = expense_df[['Amount', 'Date']]
        income_df = income_df[['Amount', 'Date']]

        temp = pd.to_datetime(expense_df['Date'])
        temp2 = pd.to_datetime(income_df['Date'])

        expense_df['Date'] = temp
        income_df['Date'] = temp2

        expense_df = expense_df[expense_df['Date'].dt.year == year]
        income_df = income_df[income_df['Date'].dt.year == year]

        if expense_df.empty or income_df.empty:

            print("No data available for the specified year after filtering.")
            return

        # Group by month and sum the amounts
        expense_df = expense_df.groupby(expense_df['Date'].dt.to_period('M')).sum(numeric_only=True)
        income_df = income_df.groupby(income_df['Date'].dt.to_period('M')).sum(numeric_only=True)

        # Plotting
        fig, ax = plt.subplots()

        # Bar plot for expenses and incomes
        ax.bar(expense_df.index.to_timestamp() - pd.DateOffset(days=7), expense_df['Amount'], width=14,
               label='Expenses')
        ax.bar(income_df.index.to_timestamp() + pd.DateOffset(days=7), income_df['Amount'], width=14, label='Incomes')

        # Calculate the average expenses and incomes
        avg_expenses = expense_df['Amount'].mean()
        avg_incomes = income_df['Amount'].mean()

        # Plotting the average lines
        ax.axhline(avg_expenses, color='red', linestyle='--', linewidth=2, label=f'Avg Expenses: {avg_expenses:.2f}zł')
        ax.axhline(avg_incomes, color='blue', linestyle='--', linewidth=2, label=f'Avg Incomes: {avg_incomes:.2f}zł')

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # Add labels and legend
        ax.set_title(f'{year}', loc='right')
        ax.set_ylabel('Amount (zł)')
        ax.legend()

        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig, ax

    def plot_income_expense_trends(self, year, month=None):
        expense_df = pd.DataFrame(self.user_expenses_list,
                                  columns=['ID', 'Amount', 'Category', 'Payment', 'Date', 'Recipe'])
        income_df = pd.DataFrame(self.user_incomes_list, columns=['ID', 'Amount', 'From', 'Date'])

        # Convert the Date columns to datetime, coerce errors to NaT
        expense_df['Date'] = pd.to_datetime(expense_df['Date'])
        income_df['Date'] = pd.to_datetime(income_df['Date'])

        # Drop rows with NaT in the 'Date' column
        expense_df = expense_df.dropna(subset=['Date'])
        income_df = income_df.dropna(subset=['Date'])

        # Filter the data for the specified year
        expense_df = expense_df[expense_df['Date'].dt.year == year]
        income_df = income_df[income_df['Date'].dt.year == year]

        # Group by month and sum the amounts
        expense_df = expense_df.groupby(expense_df['Date'].dt.to_period('M')).sum(numeric_only=True).sort_index()
        income_df = income_df.groupby(income_df['Date'].dt.to_period('M')).sum(numeric_only=True).sort_index()

        # Plotting
        fig, ax = plt.subplots()

        # Line plot for expenses and incomes
        ax.plot(expense_df.index.to_timestamp(), expense_df['Amount'], label='Expenses', marker='o', linestyle='-', color='red')
        ax.plot(income_df.index.to_timestamp(), income_df['Amount'], label='Incomes', marker='o', linestyle='-', color='green')

        # Adding a trend line for expenses
        z_expenses = np.polyfit(expense_df.index.to_timestamp().astype(int) / 10**9, expense_df['Amount'], 1)
        p_expenses = np.poly1d(z_expenses)
        ax.plot(expense_df.index.to_timestamp(), p_expenses(expense_df.index.to_timestamp().astype(int) / 10**9), "r--", label='Expenses Trend Line')

        # Adding a trend line for incomes
        z_incomes = np.polyfit(income_df.index.to_timestamp().astype(int) / 10**9, income_df['Amount'], 1)
        p_incomes = np.poly1d(z_incomes)
        ax.plot(income_df.index.to_timestamp(), p_incomes(income_df.index.to_timestamp().astype(int) / 10**9), "g--", label='Incomes Trend Line')

        # Formatting the x-axis
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # Add labels and legend
        ax.set_title(f'{year}', loc='right')
        ax.set_ylabel('Amount (zł)')
        ax.legend()

        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig, ax

    def plot_box_plot_expenses_incomes(self, year, month):
        expense_df = pd.DataFrame(self.user_expenses_list,
                                  columns=['ID', 'Amount', 'Category', 'Payment', 'Date', 'Recipe'])
        income_df = pd.DataFrame(self.user_incomes_list, columns=['ID', 'Amount', 'From', 'Date'])

        # Convert the Date columns to datetime, coerce errors to NaT
        expense_df['Date'] = pd.to_datetime(expense_df['Date'])
        income_df['Date'] = pd.to_datetime(income_df['Date'])

        # Drop rows with NaT in the 'Date' column
        expense_df = expense_df.dropna(subset=['Date'])
        income_df = income_df.dropna(subset=['Date'])

        # Filter the data for the specified year
        expense_df = expense_df[expense_df['Date'].dt.year == year]
        income_df = income_df[income_df['Date'].dt.year == year]

        # Check if DataFrames are empty after filtering
        if expense_df.empty or income_df.empty:
            print("No data available for the specified year after filtering.")
            return

        # Plotting
        fig, ax = plt.subplots()

        # Combine expenses and incomes into a single DataFrame for plotting
        combined_df = pd.DataFrame({
            'Expenses': expense_df['Amount'],
            'Incomes': income_df['Amount']
        })

        # Plotting box plot
        combined_df.plot.box(ax=ax)

        # Add labels and title
        ax.set_title(f'{year}', loc='right')
        ax.set_ylabel('Amount (zł)')

        plt.grid(True)
        plt.tight_layout()

        # Save the plot as an image file
        return fig, ax



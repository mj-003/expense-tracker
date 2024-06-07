from datetime import datetime

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from financials.user_expenses import UserExpenses
from financials.user_incomes import UserIncomes


class MyPlotter:
    def __init__(self, user_expenses: UserExpenses, user_incomes: UserIncomes):
        self.user_expenses_list = user_expenses.get_expenses()[1:]
        self.user_incomes_list = user_incomes.get_incomes()[1:]
        self.amount_column = 1
        self.category_column = 2
        self.date_column = 4

    def get_incomes_expenses_pd(self):
        """
        Function to get incomes and expenses as pandas dataframes
        :return:
        """
        incomes_pd = pd.DataFrame(self.user_incomes_list, columns=["ID", "Amount", "From", "Date", "Description"])
        expenses_pd = pd.DataFrame(self.user_expenses_list,
                                   columns=["ID", "Amount", "Category", "Payment method", "Date", "Photo path",
                                            "Description"])
        incomes_pd['Date'] = pd.to_datetime(incomes_pd['Date'])
        expenses_pd['Date'] = pd.to_datetime(expenses_pd['Date'])

        return incomes_pd, expenses_pd

    def plot_category_pie_chart(self, month, year=None):
        """
        Function to plot a pie chart of expenses by category for a given month
        :param month:
        :param year:
        :return:
        """
        colors = ['#8fbc8f', '#006400', '#228b22', '#679267', '#7bb661', '#8fbc8f', '#addfad']

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
        plt.title(f'{month}', loc='left')

        return fig, ax

    def plot_incomes_expenses_per_month(self, month, incomes_list, expenses_list):
        """
        Function to plot a bar chart of total incomes and expenses for a given month
        :param month:
        :param incomes_list:
        :param expenses_list:
        :return:
        """

        incomes_pd, expenses_pd = self.get_incomes_expenses_pd()

        incomes_pd = incomes_pd[incomes_pd['Date'].dt.strftime('%Y-%m') == month]
        expenses_pd = expenses_pd[expenses_pd['Date'].dt.strftime('%Y-%m') == month]
        total_income = incomes_pd['Amount'].sum()
        total_expenses = expenses_pd['Amount'].sum()

        fig, ax = plt.subplots(figsize=(3, 2))

        fig.patch.set_facecolor('#eeeeee')
        ax.set_facecolor('#eeeeee')

        categories = ['Income', 'Expenses']
        amounts = [total_income, total_expenses]
        colors = ['#2A8C55', '#207244']

        # Plot the bars and add text
        bars = ax.bar(categories, amounts, color=colors, edgecolor='none')
        for i, amount in enumerate(amounts):
            ax.text(i, amount, f'{amount:.2f}', ha='center', va='bottom')

        # Remove the spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Set limits and labels
        ax.set_xlim(-0.5, len(categories) - 0.5)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories)
        ax.set_yticklabels([])
        ax.yaxis.set_visible(False)
        month_name = datetime.strptime(month, '%Y-%m').strftime('%b')
        ax.set_title(month_name, loc='right', fontsize=10)

        return fig, ax

    def get_expenses_by_month(self, month) -> list:
        """
        Function to filter expenses by month
        :param month:
        :return:
        """
        filtered_expenses = []
        for expense in self.user_expenses_list:
            if expense[self.date_column][:7] == month:
                filtered_expenses.append(expense)

        return filtered_expenses

    def plot_expenses_incomes(self, year, month=None):
        """
        Function to plot a bar chart of total expenses and incomes for a given month
        :param year:
        :param month:
        :return:
        """
        income_df, expense_df = self.get_incomes_expenses_pd()

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
               label='Expenses', color='#8fbc8f')
        ax.bar(income_df.index.to_timestamp() + pd.DateOffset(days=7), income_df['Amount'], width=14, label='Incomes', color='#006400')

        # Calculate the average expenses and incomes
        avg_expenses = expense_df['Amount'].mean()
        avg_incomes = income_df['Amount'].mean()

        # Plotting the average lines
        ax.axhline(avg_expenses, color='#228b22', linestyle='--', linewidth=2, label=f'Avg Expenses: {avg_expenses:.2f} zł')
        ax.axhline(avg_incomes, color='#679267', linestyle='--', linewidth=2, label=f'Avg Incomes: {avg_incomes:.2f} zł')

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # Add labels and legend
        ax.set_title(f'{year}', loc='right')
        ax.legend()

        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig, ax

    def plot_income_expense_trends(self, year, month=None):
        """
        Function to plot a line chart of total expenses and incomes for a given year
        :param year:
        :param month:
        :return:
        """
        income_df, expense_df = self.get_incomes_expenses_pd()
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
        ax.plot(expense_df.index.to_timestamp(), expense_df['Amount'], label='Expenses', marker='o', linestyle='-',
                color='#8fbc8f')
        ax.plot(income_df.index.to_timestamp(), income_df['Amount'], label='Incomes', marker='o', linestyle='-',
                color='#006400')

        # Adding a trend line for expenses
        z_expenses = np.polyfit(expense_df.index.to_timestamp().astype(int) / 10 ** 9, expense_df['Amount'], 1)
        p_expenses = np.poly1d(z_expenses)
        ax.plot(expense_df.index.to_timestamp(), p_expenses(expense_df.index.to_timestamp().astype(int) / 10 ** 9),
                "r--", label='Expenses Trend Line', color='#228b22')

        # Adding a trend line for incomes
        z_incomes = np.polyfit(income_df.index.to_timestamp().astype(int) / 10 ** 9, income_df['Amount'], 1)
        p_incomes = np.poly1d(z_incomes)
        ax.plot(income_df.index.to_timestamp(), p_incomes(income_df.index.to_timestamp().astype(int) / 10 ** 9), "g--",
                label='Incomes Trend Line', color='#8db600')

        # Formatting the x-axis
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # Add labels and legend
        ax.set_title(f'{year}', loc='right')
        ax.legend()

        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig, ax

    def plot_box_plot_expenses_incomes(self, year, month):
        """
        Function to plot a box plot of expenses and incomes for a given year
        :param year:
        :param month:
        :return:
        """
        income_df, expense_df = self.get_incomes_expenses_pd()

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

        plt.grid(True)
        plt.tight_layout()

        # Save the plot as an image file
        return fig, ax

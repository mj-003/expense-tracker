import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

class ExpenseIncomePlotter:
    def __init__(self, user_expenses_list, user_incomes_list):
        self.user_expenses_list = user_expenses_list
        self.user_incomes_list = user_incomes_list

    def plot_expenses_incomes(self, year):
        # Convert lists of lists to DataFrames
        expense_df = pd.DataFrame(self.user_expenses_list, columns=['Amount', 'Date'])
        income_df = pd.DataFrame(self.user_incomes_list, columns=['Amount', 'Date'])

        # Convert the Date columns to datetime, coerce errors to NaT
        expense_df['Date'] = pd.to_datetime(expense_df['Date'], errors='coerce')
        income_df['Date'] = pd.to_datetime(income_df['Date'], errors='coerce')

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

        # Group by month and sum the amounts
        expense_df = expense_df.groupby(expense_df['Date'].dt.to_period('M')).sum(numeric_only=True).sort_index()
        income_df = income_df.groupby(income_df['Date'].dt.to_period('M')).sum(numeric_only=True).sort_index()

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))

        # Bar plot for expenses and incomes
        ax.bar(expense_df.index.to_timestamp() - pd.DateOffset(days=7), expense_df['Amount'], width=14, label='Expenses')
        ax.bar(income_df.index.to_timestamp() + pd.DateOffset(days=7), income_df['Amount'], width=14, label='Incomes')

        # Calculate the average expenses and incomes
        avg_expenses = expense_df['Amount'].mean()
        avg_incomes = income_df['Amount'].mean()

        # Plotting the average lines
        ax.axhline(avg_expenses, color='red', linestyle='--', linewidth=2, label=f'Avg Expenses: ${avg_expenses:.2f}')
        ax.axhline(avg_incomes, color='blue', linestyle='--', linewidth=2, label=f'Avg Incomes: ${avg_incomes:.2f}')

        # Formatting the x-axis
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # Add labels and legend
        ax.set_title(f'Monthly Expenses and Incomes for {year}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Amount ($)')
        ax.legend()

        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot as an image file
        plt.show()

# Example usage with sample data containing more columns
user_expenses_list = [
    [100.0, '2024-06-02'], [23.49, '2024-06-02'], [29.98, '2024-06-02'],
    [34.0, '2024-06-02'], [239.99, '2024-06-02'], [20.99, '2024-06-02'],
    [987.0, '2024-06-02'], [223.0, '2024-06-02'], [177.0, '2024-05-09'],
    [199.0, '2024-05-03'], [13.0, '2024-05-03'], [333.0, '2024-06-02'],
    [99.0, '2024-06-02'], [9.0, '2024-06-02'], [33.0, '2024-06-02'],
    [44.0, '2024-06-02'], [33.0, '2024-06-02'], [44.0, '2024-06-02'],
    [1000.0, '2024-06-06'], [100.0, '2024-06-01'], [10.0, '2024-06-01'],
    [100.0, '2024-06-28'], [20.0, '2024-06-01'], [20.0, '2024-06-01'],
    [100.0, '2024-06-01'], [100.0, '2024-06-01'], [99.0, '2024-06-01'],
    [10.0, '2024-06-01'], [100.0, '2024-06-01'], [100.0, '2024-06-01'],
    [100.0, '2024-05-10'], [100.0, '2024-06-01'], [11.0, '2024-05-31'],
    [25.0, '2024-06-02']
]

user_incomes_list = [
    [99999.99, '2024-06-02'], [888.0, '2024-06-02'], [122.0, '2024-06-02'],
    [299.0, '2024-06-02'], [100.0, '2024-06-01'], [100.0, '2024-06-01'],
    [1.0, '2024-06-01'], [50.0, '2024-05-10'], [50.0, '2024-05-09'],
    [50.0, '2024-05-09'], [50.0, '2024-05-08'], [30.0, '2024-05-07'],
    [30.0, '2024-05-06'], [15.0, '2024-05-05'], [15.0, '2024-06-02'],
    [19.0, '2024-06-02']
]

plotter = ExpenseIncomePlotter(user_expenses_list, user_incomes_list)
plotter.plot_expenses_incomes(2024)

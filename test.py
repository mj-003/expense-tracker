import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np


def plot_box_plot_expenses_incomes(user_expenses_list, user_incomes_list, year):
    # Convert lists of lists to DataFrames
    expense_df = pd.DataFrame(user_expenses_list, columns=['Amount', 'Date'])
    income_df = pd.DataFrame(user_incomes_list, columns=['Amount', 'Date'])

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

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Combine expenses and incomes into a single DataFrame for plotting
    combined_df = pd.DataFrame({
        'Expenses': expense_df['Amount'],
        'Incomes': income_df['Amount']
    })

    # Plotting box plot
    combined_df.plot.box(ax=ax)

    # Add labels and title
    ax.set_title(f'Box Plot of Monthly Expenses and Incomes for {year}', pad=20)
    ax.set_ylabel('Amount ($)')

    plt.grid(True)
    plt.tight_layout()

    # Save the plot as an image file
    plt.show()


# Example usage with sample data
user_expenses_list = [
    [100.0, '2024-06-02'], [23.49, '2024-06-02'], [29.98, '2024-06-02'],
    [34.0, '2024-07-02'], [239.99, '2024-07-02'], [20.99, '2024-07-02'],
    [987.0, '2024-08-02'], [223.0, '2024-08-02'], [177.0, '2024-08-09'],
    [199.0, '2024-09-03'], [13.0, '2024-09-03'], [333.0, '2024-09-02'],
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
    [99.99, '2024-06-02'], [888.0, '2024-06-02'], [122.0, '2024-06-02'],
    [299.0, '2024-07-02'], [100.0, '2024-07-01'], [100.0, '2024-07-01'],
    [1.0, '2024-08-01'], [50.0, '2024-08-10'], [50.0, '2024-08-09'],
    [50.0, '2024-09-09'], [50.0, '2024-09-08'], [30.0, '2024-09-07'],
    [30.0, '2024-05-06'], [15.0, '2024-05-05'], [15.0, '2024-06-02'],
    [19.0, '2024-06-02']
]

plot_box_plot_expenses_incomes(user_expenses_list, user_incomes_list, 2024)

from expenses.user_expenses import UserExpenses
from utils.exports import export_to_excel, export_to_csv
from datetime import datetime


class PageController:
    def __init__(self, database, user, user_expenses: UserExpenses):
        self.user_expenses = user_expenses
        print('--------dupa dupa--------')
        print(user_expenses)

    def get_filtered_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        return self.user_expenses.get_expenses(date_filter, category_filter, sort_order)

    def export_data(self, file_path):
        if file_path.endswith('.xlsx'):
            export_to_excel(file_path, self.user_expenses.expenses)
        elif file_path.endswith('.csv'):
            export_to_csv(file_path, self.user_expenses.expenses)

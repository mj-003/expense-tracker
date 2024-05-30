from datetime import datetime
from .user_finances import UserFinancials

headers = [['No.', 'Amount', 'Category', 'Payment method', 'Date']]


class UserExpenses(UserFinancials):
    def __init__(self, database, user):
        super().__init__(database, user)

    def load_expenses(self):
        self.load_items()

    def add_expense(self, expense):
        self.add_item(expense, self.database.add_expense)

    def get_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        filtered_expenses = self.items[:]

        if date_filter:
            filtered_expenses = self.filter_by_date(filtered_expenses, date_filter)

        if category_filter and category_filter != "Category":
            filtered_expenses = [expense for expense in filtered_expenses if expense[2] == category_filter]

        if sort_order:
            reverse = sort_order.split()[0] == "⬇"
            if sort_order != 'Sort':

                if sort_order.split()[1] == "Amount":
                    filtered_expenses.sort(key=lambda x: x[1], reverse=reverse)
                elif sort_order.split()[1] == "Time":
                    filtered_expenses.sort(key=lambda x: datetime.strptime(x[4], '%Y-%m-%d'), reverse=reverse)

        return headers + filtered_expenses

    def get_expense(self, autonumbered_id):
        self.get_item(autonumbered_id, self.database.get_expenses)

    def filter_by_date(self, expenses, date_filter):
        if date_filter == "This month":
            start_date = datetime.now().replace(day=1)
        elif date_filter == "This year":
            start_date = datetime.now().replace(month=1, day=1)
        else:
            return expenses

        return [expense for expense in expenses if datetime.strptime(expense[4], '%Y-%m-%d') >= start_date]

    def delete_expense(self, autonumbered_id):
        self.delete_item(autonumbered_id, self.database.del_expense)

    def update_user_expense(self, autonumbered_id, updated_expense):
        self.update_item(autonumbered_id, updated_expense, self.database.update_expense)
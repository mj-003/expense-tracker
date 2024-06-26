from datetime import datetime
from .user_finances import UserFinancials


class UserExpenses(UserFinancials):
    def __init__(self, database, user):
        super().__init__(database, user)
        self.load_expenses()
        self.headers = self.get_headers()

    def get_headers(self):
        """
        Get the headers        :return:
        """
        return [['No.', f'Amount {self.currency}', 'Category', 'Payment method', 'Date']]

    def load_expenses(self):
        """
        Load expenses from the database
        :return: None
        """
        self.load_items(self.database.get_expenses)

    def add_expense(self, expense):
        """
        Add an expense to the database
        :param expense: Expense
        :return: None
        """
        self.add_item(expense, self.database.add_expense, self.database.get_expenses)

    def get_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        """
        Get expenses from the database, filtered and sorted
        :param date_filter: date filter, default None, might be "This month", "This year"
        :param category_filter: category filter, default None, might be "Food", "Transport", "Entertainment", "Other"
        :param sort_order: sort order, default None, might be ascending or descending, for date or amount
        :return: list of filtered and sorted expenses
        """
        filtered_expenses = self.items[:]

        if date_filter:
            filtered_expenses = self.filter_by_date(filtered_expenses, date_filter)

        if category_filter and category_filter != "Categories":
            filtered_expenses = [expense for expense in filtered_expenses if expense[2] == category_filter]

        if sort_order:
            filtered_expenses = self.sort_items(items=filtered_expenses, sort_order=sort_order, date_index=4)

        self.headers = self.get_headers()
        return self.headers + filtered_expenses

    def get_expense(self, autonumbered_id):
        """
        Get an expense by autonumbered ID
        :param autonumbered_id: ID of the expense
        :return: expense
        """
        item_id = self.get_item_id(autonumbered_id, self.database.get_expenses)
        if item_id:
            return self.database.get_expense(item_id)
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")
            return None

    def filter_by_date(self, expenses, date_filter):
        """
        Filter expenses by date
        :param expenses: list of expenses
        :param date_filter: date filter, might be "This month", "This year"
        :return: list of filtered expenses
        """
        if date_filter == "This month":
            start_date = datetime.now().replace(day=1)
        elif date_filter == "This year":
            start_date = datetime.now().replace(month=1, day=1)
        else:
            return expenses
        # expense[4] - date
        return [expense for expense in expenses if datetime.strptime(expense[4], '%Y-%m-%d') >= start_date]

    def delete_expense(self, autonumbered_id):
        """
        Delete an expense by autonumbered ID
        :param autonumbered_id: ID of the expense
        :return: None
        """
        self.delete_item(autonumbered_id, self.database.del_expense, self.database.get_expenses)

    def update_user_expense(self, autonumbered_id, updated_expense):
        """
        Update an expense by autonumbered ID
        :param autonumbered_id: ID of the expense
        :param updated_expense: updated expense
        :return: None
        """
        self.update_item(autonumbered_id, updated_expense, self.database.update_expense, self.database.get_expenses)

    def get_sum(self):
        """
        Get the sum of expenses for the current month
        :return: sum of expenses
        """
        # expense[1] - amount
        # expense[4] - date
        return sum([expense[1] for expense in self.items if datetime.strptime(expense[4], '%Y-%m-%d').month == datetime.today().month])
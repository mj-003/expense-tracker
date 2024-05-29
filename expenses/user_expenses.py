from datetime import datetime

headers = [['No.', 'Amount', 'Category', 'Description', 'Payment method', 'Date']]

class UserExpenses:
    def __init__(self, database, user):
        self.database = database
        self.user = user
        self.expenses = []
        self.original_ids = []  # Przechowuje oryginalne ID z bazy danych
        self.load_expenses()

    def __len__(self):
        return len(self.expenses)

    def load_expenses(self):
        user_id = self.database.get_user_id(self.user.username)
        expenses_from_db = self.database.get_expenses(user_id)
        self.expenses = []
        self.original_ids = []

        for idx, expense in enumerate(expenses_from_db):
            self.original_ids.append(expense[0])
            autonumbered_expense = [idx + 1] + list(expense[2:])
            self.expenses.append(autonumbered_expense)

        print('--------start--------')
        print(self.expenses)
        print('--------stop--------')

    def add_expense(self, expense):
        self.database.add_expense(self.user.id, expense)
        self.load_expenses()

    def get_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        filtered_expenses = self.expenses[:]

        if date_filter:
            filtered_expenses = self.filter_by_date(filtered_expenses, date_filter)

        if category_filter and category_filter != "Category":
            filtered_expenses = [expense for expense in filtered_expenses if expense[2] == category_filter]

        if sort_order:
            reverse = sort_order.split()[0] == "⬇"

            if sort_order.split()[1] == "Amount":
                filtered_expenses.sort(key=lambda x: x[1], reverse=reverse)
            elif sort_order.split()[1] == "Time":
                filtered_expenses.sort(key=lambda x: datetime.strptime(x[5], '%Y-%m-%d'), reverse=reverse)

        return headers + filtered_expenses

    def filter_by_date(self, expenses, date_filter):
        if date_filter == "This month":
            start_date = datetime.now().replace(day=1)
        elif date_filter == "This year":
            start_date = datetime.now().replace(month=1, day=1)
        else:
            return expenses

        return [expense for expense in expenses if datetime.strptime(expense[5], '%Y-%m-%d') >= start_date]

    def delete_expense(self, autonumbered_id):
        if 0 < autonumbered_id <= len(self.original_ids):
            expense_id = self.original_ids[autonumbered_id - 1]
            self.database.del_expense(expense_id)
            self.load_expenses()
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")

    def update_expense(self, autonumbered_id, updated_expense):
        if 0 < autonumbered_id <= len(self.original_ids):
            expense_id = self.original_ids[autonumbered_id - 1]
            self.database.update_expense(expense_id, updated_expense)
            self.load_expenses()
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")
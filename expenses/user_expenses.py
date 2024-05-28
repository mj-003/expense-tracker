from datetime import datetime


class UserExpenses:
    def __init__(self, database, user):
        self.database = database
        self.user = user
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        user_id = self.database.get_user_id(self.user.username)
        self.expenses = self.database.get_expenses(user_id)
        for i in range(len(self.expenses)):
            self.expenses[i] = list(self.expenses[i])[2:]
        print('--------start--------')
        print(self.expenses)
        print('--------stop--------')

    def add_expense(self, expense):
        self.database.add_expense(self.user.id, expense)
        self.load_expenses()

    def get_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        filtered_expenses = self.expenses

        if date_filter:
            filtered_expenses = self.filter_by_date(date_filter)

        if category_filter:
            filtered_expenses = [expense for expense in filtered_expenses if expense[0] == category_filter]

        if sort_order:
            reverse = sort_order == "Descending"
            filtered_expenses.sort(key=lambda x: x[4], reverse=reverse)

        return filtered_expenses

    def filter_by_date(self, date_filter):
        if date_filter == "This month":
            start_date = datetime.now().replace(day=1)
        elif date_filter == "This year":
            start_date = datetime.now().replace(month=1, day=1)
        else:
            return self.expenses

        return [expense for expense in self.expenses if datetime.strptime(expense[4], '%Y-%m-%d') >= start_date]


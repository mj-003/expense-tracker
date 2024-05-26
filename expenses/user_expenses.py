class UserExpenses:
    def __init__(self, user_id):
        self.user_id = user_id
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    def get_expenses(self):
        return self.expenses

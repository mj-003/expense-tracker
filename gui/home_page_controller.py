from datetime import datetime

from financials.user_expenses import UserExpenses
from financials.user_incomes import UserIncomes


class HomePageController:
    def __init__(self, user_expenses: UserExpenses, user_incomes: UserIncomes):
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        print(self.user_expenses.get_expenses())
        print(self.user_incomes.get_incomes())

    def create_user_items_list(self):
        cat_names = ['No.', 'Amount (zł)', 'Category', 'Date']
        user_expenses_list = self.user_expenses.get_expenses()
        user_incomes_list = self.user_incomes.get_incomes()
        user_items_list = [cat_names]

        for i, expense in enumerate(user_expenses_list[1:]):
            user_items_list.append([i + 1] + [expense[1]] + ['Expense'] + [expense[4]])
        for i, income in enumerate(user_incomes_list[1:]):
            user_items_list.append([len(user_items_list) + 1] + [income[1]] + ['Income'] + [income[3]])
        print(user_items_list)
        return user_items_list

    def get_filtered_items(self, items_list, date=None, category=None, sort=None):
        headers = [items_list[0]]
        filtered_items = items_list[1:]
        if date:
            if date == 'This month':
                date = datetime.now().replace(day=1)
                filtered_items = [item for item in filtered_items if datetime.strptime(item[3], '%Y-%m-%d') >= date]
            elif date == 'This year':
                date = datetime.now().replace(month=1, day=1)
                filtered_items = [item for item in filtered_items if datetime.strptime(item[3], '%Y-%m-%d') >= date]
        if category:
            if category == 'Expenses':
                filtered_items = [item for item in filtered_items if item[2] == 'Expense']
            if category == 'Incomes':
                filtered_items = [item for item in filtered_items if item[2] == 'Income']
        if sort:
            reverse = sort.split()[0] == "⬇"
            if sort != 'Sort':

                if sort.split()[1] == "Amount":
                    filtered_items.sort(key=lambda x: x[1], reverse=reverse)
                elif sort.split()[1] == "Time":
                    filtered_items.sort(key=lambda x: datetime.strptime(x[3], '%Y-%m-%d'), reverse=reverse)
        return headers + filtered_items

    def get_chart_data(self, current_month):
        month_str = current_month.strftime('%Y-%m')
        incomes_list = self.user_incomes.get_incomes()[1:]  # Assuming first element is header or meta
        expenses_list = self.user_expenses.get_expenses()[1:]  # Assuming first element is header or meta
        return month_str, incomes_list, expenses_list

    def get_filtered_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        return self.user_expenses.get_expenses(date_filter, category_filter, sort_order)

    def get_filtered_incomes(self, date=None, from_who=None, sort=None):
        print(self.user_incomes.get_incomes())
        return self.user_incomes.get_incomes(date, from_who, sort)

    def check_if_available(self, year):
        for item in self.user_expenses.get_expenses()[1:]:
            if item[4][:4] == str(year):
                print("Available", str(year))
                return True
        for item in self.user_incomes.get_incomes()[1:]:
            if item[3][:4] == str(year):
                return True
        return False

    def check_if_available_month(self, month):
        for item in self.user_expenses.get_expenses()[1:]:
            if item[4][:7] == month:
                return True
        for item in self.user_incomes.get_incomes()[1:]:
            if item[3][:7] == month:
                return True
        return False







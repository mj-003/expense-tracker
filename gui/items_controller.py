from datetime import datetime

from financials.user_expenses import UserExpenses
from financials.user_incomes import UserIncomes


class ItemsController:
    def __init__(self, user_expenses: UserExpenses, user_incomes: UserIncomes, currency):

        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        self.currency = currency

    def create_user_items_list(self):
        """
        Create a list of items for the user
        :return:
        """
        cat_names = ['No.', f'Amount {self.currency}', 'Category', 'Date']
        user_expenses_list = self.user_expenses.get_expenses()
        user_incomes_list = self.user_incomes.get_incomes()
        user_items_list = [cat_names]

        # Add expenses to the list
        for i, expense in enumerate(user_expenses_list[1:]):
            user_items_list.append([i + 1] + [expense[1]] + ['Expense'] + [expense[4]])
        for i, income in enumerate(user_incomes_list[1:]):
            user_items_list.append([len(user_items_list) + 1] + [income[1]] + ['Income'] + [income[3]])
        return user_items_list

    def get_filtered_items(self, items_list, date=None, category=None, sort=None):
        """
        Filter the items list based on the filters
        :param items_list:
        :param date:
        :param category:
        :param sort:
        :return:
        """
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
        """
        Get the chart data
        :param current_month:
        :return:
        """
        month_str = current_month.strftime('%Y-%m')
        incomes_list = self.user_incomes.get_incomes()[1:]  # first row is header
        expenses_list = self.user_expenses.get_expenses()[1:]   # first row is header
        return month_str, incomes_list, expenses_list

    def get_filtered_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        """
        Get the filtered expenses
        :param date_filter:
        :param category_filter:
        :param sort_order:
        :return:
        """
        return self.user_expenses.get_expenses(date_filter, category_filter, sort_order)

    def get_filtered_incomes(self, date=None, from_who=None, sort=None):
        """
        Get the filtered incomes
        :param date:
        :param from_who:
        :param sort:
        :return:
        """
        return self.user_incomes.get_incomes(date, from_who, sort)

    def check_if_available(self, year):
        """
        Check if data is available for the selected year
        :param year:
        :return:
        """
        for item in self.user_expenses.get_expenses()[1:]:
            if item[4][:4] == str(year):
                print("Available", str(year))
                return True
        for item in self.user_incomes.get_incomes()[1:]:
            if item[3][:4] == str(year):
                return True
        return False

    def check_if_available_month(self, month):
        """
        Check if data is available for the selected month
        :param month:
        :return:
        """
        for item in self.user_expenses.get_expenses()[1:]:
            print(item[4][:7], month)
            if item[4][:7] == month:
                return True
        for item in self.user_incomes.get_incomes()[1:]:
            if item[3][:7] == month:
                return True
        return False

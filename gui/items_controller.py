from datetime import datetime

from financials.user_expenses import UserExpenses
from financials.user_incomes import UserIncomes


class ItemsController:
    """

    Class ItemsController.
    This class is responsible for handling the items of the user.
    Especially combined expenses and incomes.
    This class is used in the HomePage and ExportPage class
    (where are used combined expenses and incomes).

    """
    def __init__(self, user_expenses: UserExpenses, user_incomes: UserIncomes, currency):

        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        self.currency = currency

    def create_user_items_list(self):
        """

        Create the user items list by combining the expenses and incomes.

        """
        # headers
        cat_names = ['No.', f'Amount {self.currency}', 'Category', 'Date']

        # Get the expenses and incomes
        user_expenses_list = self.user_expenses.get_expenses()
        user_incomes_list = self.user_incomes.get_incomes()

        # Create the user items list
        user_items_list = [cat_names]

        # Add expenses to the list
        for i, expense in enumerate(user_expenses_list[1:]):
            user_items_list.append([i + 1] + [expense[1]] + ['Expense'] + [expense[4]])
        for i, income in enumerate(user_incomes_list[1:]):
            user_items_list.append([len(user_items_list) + 1] + [income[1]] + ['Income'] + [income[3]])
        return user_items_list

    def get_filtered_items(self, items_list, date=None, category=None, sort=None):
        """

        Filter the items list by date, category and sort order.

        :param items_list: list of items
        :param date: date filter, default None, might be 'This month', 'This year'
        :param category: category filter, default None, might be 'Expenses', 'Incomes' or 'Both'
        :param sort: sort order, default None, sort might be ascending or descending for amount and date

        :return: filtered items list
        """
        headers = [items_list[0]]
        filtered_items = items_list[1:]

        # item[3] - date
        # item[2] - category
        # item[1] - amount

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

        Get the chart data for the current month.

        :param current_month: current month

        :return: month in string format, incomes list, expenses list
        """
        month_str = current_month.strftime('%Y-%m')
        incomes_list = self.user_incomes.get_incomes()[1:]  # first row is header
        expenses_list = self.user_expenses.get_expenses()[1:]   # first row is header
        return month_str, incomes_list, expenses_list

    def get_filtered_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        """

        Get the filtered expenses based on the date, category and sort order.

        :param date_filter: date filter, default None, might be 'This month', 'This year'
        :param category_filter: category filter, default None
        :param sort_order: sort order, default None, might be ascending or descending for amount and date

        :return: filtered and sorted expenses list
        """
        return self.user_expenses.get_expenses(date_filter, category_filter, sort_order)

    def get_filtered_incomes(self, date=None, from_who=None, sort=None):
        """

        Get the filtered incomes based on the date, from who and sort order.

        :param date: date filter, default None, might be 'This month', 'This year'
        :param from_who: from who filter, default None
        :param sort: sort order, default None, might be ascending or descending for amount and date

        :return: filtered and sorted incomes list
        """
        return self.user_incomes.get_incomes(date, from_who, sort)

    def check_if_available(self, year):
        """

        Check if data is available for the selected year.

        :param year: year that needs to be checked

        :return: True if data is available, False otherwise
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

        :param month: month that needs to be checked

        :return: True if data is available, False otherwise
        """
        for item in self.user_expenses.get_expenses()[1:]:
            print(item[4][:7], month)
            if item[4][:7] == month:
                return True
        for item in self.user_incomes.get_incomes()[1:]:
            if item[3][:7] == month:
                return True
        return False

from abc import abstractmethod

from financials.user_expenses import UserExpenses
from financials.user_incomes import UserIncomes


class ItemPageController:
    def __init__(self, database, user, user_expenses: UserExpenses, user_incomes: UserIncomes):
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        self.user = user
        self.database = database

    @abstractmethod
    def get_filtered_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        return self.user_expenses.get_expenses(date_filter, category_filter, sort_order)

    @abstractmethod
    def get_filtered_items(self, items_list, date, category, sort):
        pass

    @abstractmethod
    def get_filtered_incomes(self, date=None, from_who=None, sort=None):
        return self.user_incomes.get_incomes(date, from_who, sort)

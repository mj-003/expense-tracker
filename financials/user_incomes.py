from datetime import datetime
from .user_finances import UserFinancials


class UserIncomes(UserFinancials):
    def __init__(self, database, user):
        super().__init__(database, user)
        self.load_incomes()
        self.headers = self.get_headers()

    def get_headers(self):
        """
        Get the headers for the incomes
        :return: headers, as a list of lists
        """
        return [['No.', f'Amount {self.currency}', 'From', 'Date']]

    def load_incomes(self):
        """
        Load incomes from the database
        :return: None
        """
        self.load_items(self.database.get_incomes)

    def add_income(self, income):
        """
        Add an income to the database
        :param income: income to add
        :return: None
        """
        self.add_item(income, self.database.add_income, self.database.get_incomes)

    def get_income(self, autonumbered_id: int) -> None:
        """
        Get an income by autonumbered ID
        :param autonumbered_id: autonumbered ID of the income
        :return: income from the database, or None if the ID is invalid
        """
        item_id = self.get_item_id(autonumbered_id, self.database.get_incomes)
        if item_id:
            return self.database.get_income(item_id)
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")
            return None

    def get_incomes(self, date_filter=None, from_filter=None, sort_order=None) -> list:
        """
        Get incomes filtered and sorted incomes from the database
        :param date_filter: date filter, default is None, might be "This month" or "This year"
        :param from_filter: from filter, default is None
        :param sort_order: sort order, default is None, might be ascending or descending, for date or amount
        :return: filtered and sorted incomes
        """
        filtered_incomes = self.items[:]

        if date_filter:
            filtered_incomes = self.filter_by_date(filtered_incomes, date_filter)

        if from_filter and from_filter != "From":
            filtered_incomes = [income for income in filtered_incomes if income[2] == from_filter]

        if sort_order:
            filtered_incomes = self.sort_items(items=filtered_incomes, sort_order=sort_order, date_index=3)

        self.headers = self.get_headers()
        return self.headers + filtered_incomes

    def delete_income(self, autonumbered_id):
        """
        Delete an income by autonumbered ID
        :param autonumbered_id: autonumbered ID of the income
        :return: None
        """
        self.delete_item(autonumbered_id, self.database.del_income, self.database.get_incomes)

    def update_user_income(self, autonumbered_id, updated_income):
        """
        Update an income by autonumbered ID
        :param autonumbered_id: autonumbered ID of the income
        :param updated_income:  updated income
        :return: None
        """
        self.update_item(autonumbered_id, updated_income, self.database.update_income, self.database.get_incomes)

    def filter_by_date(self, incomes, date_filter):
        """
        Filter incomes by date
        :param incomes: list of incomes
        :param date_filter: date filter, might be "This month" or "This year"
        :return: filtered incomes
        """
        if date_filter == "This month":
            start_date = datetime.now().replace(day=1)
        elif date_filter == "This year":
            start_date = datetime.now().replace(month=1, day=1)
        else:
            return incomes

        return [income for income in incomes if datetime.strptime(income[3], '%Y-%m-%d') >= start_date]

    def update_user_incomes(self, autonumbered_id: int, updated_income) -> None:
        """
        Update an income by autonumbered ID
        :param autonumbered_id: autonumbered ID of the income
        :param updated_income: updated income
        :return: None
        """
        self.update_item(autonumbered_id, updated_income, self.database.update_income, self.database.get_incomes)

    def get_sum(self) -> float:
        """
        Get the sum of all incomes
        :return: sum of all incomes
        """
        # income[1] - amount
        # income[3] - date
        return sum([income[1] for income in self.items if datetime.strptime(income[3], '%Y-%m-%d').month == datetime.today().month])

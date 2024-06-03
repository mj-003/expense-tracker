from datetime import datetime
from .user_finances import UserFinancials

headers = [['No.', 'Amount (zł)', 'From', 'Date']]


class UserIncomes(UserFinancials):
    def __init__(self, database, user):
        super().__init__(database, user)
        self.load_incomes()

    def load_incomes(self):
        """
        Load incomes from the database
        :return:
        """
        self.load_items(self.database.get_incomes)

    def add_income(self, income):
        """
        Add an income to the database
        :param income:
        :return:
        """
        self.add_item(income, self.database.add_income, self.database.get_incomes)

    def get_income(self, autonumbered_id: int) -> None:
        """
        Get an income by autonumbered ID
        :param autonumbered_id:
        :return:
        """
        self.get_item(autonumbered_id, self.database.get_income)

    def get_incomes(self, date_filter=None, from_filter=None, sort_order=None) -> list:
        """
        Get incomes from the database
        :param date_filter:
        :param from_filter:
        :param sort_order:
        :return:
        """
        filtered_incomes = self.items[:]

        if date_filter:
            filtered_incomes = self.filter_by_date(filtered_incomes, date_filter)

        if from_filter and from_filter != "From":
            filtered_incomes = [income for income in filtered_incomes if income[2] == from_filter]

        if sort_order:
            reverse = sort_order.split()[0] == "⬇"
            if sort_order != 'Sort':

                if sort_order.split()[1] == "Amount":
                    filtered_incomes.sort(key=lambda x: x[1], reverse=reverse)
                elif sort_order.split()[1] == "Time":
                    filtered_incomes.sort(key=lambda x: datetime.strptime(x[3], '%Y-%m-%d'), reverse=reverse)

        return headers + filtered_incomes

    def delete_income(self, autonumbered_id):
        """
        Delete an income by autonumbered ID
        :param autonumbered_id:
        :return:
        """
        self.delete_item(autonumbered_id, self.database.del_income, self.database.get_incomes)

    def update_user_income(self, autonumbered_id, updated_income):
        self.update_item(autonumbered_id, updated_income, self.database.update_income)

    def filter_by_date(self, incomes, date_filter):
        """
        Filter incomes by date
        :param incomes:
        :param date_filter:
        :return:
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
        :param autonumbered_id:
        :param updated_income:
        :return:
        """
        self.update_item(autonumbered_id, updated_income, self.database.update_income, self.database.get_incomes)

    def get_sum(self) -> float:
        """
        Get the sum of all incomes
        :return:
        """
        return sum([income[1] for income in self.items if datetime.strptime(income[3], '%Y-%m-%d').month == datetime.today().month])

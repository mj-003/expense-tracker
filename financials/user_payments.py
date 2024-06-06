from datetime import datetime
from .user_finances import UserFinancials

headers = [['No.', 'Amount', 'Title', 'Date', 'How often']]


class UserPayments(UserFinancials):
    def __init__(self, database, user):
        super().__init__(database, user)
        self.load_payments()

    def load_payments(self):
        """
        Load incomes from the database
        :return:
        """
        self.load_items(self.database.get_payments)

    def add_payment(self, payment):
        """
        Add an income to the database
        :param payment:
        :return:
        """
        self.add_item(payment, self.database.add_payment, self.database.get_payments)

    def get_payment(self, autonumbered_id: int) -> None:
        """
        Get an income by autonumbered ID
        :param autonumbered_id:
        :return:
        """
        if 0 < autonumbered_id <= len(self.original_ids):
            item_id = self.original_ids[autonumbered_id - 1]
            return self.database.get_payment(item_id)
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")
            return None

    def get_payments(self, date_filter=None, from_filter=None, sort_order=None) -> list:
        """
        Get incomes from the database
        :param date_filter:
        :param from_filter:
        :param sort_order:
        :return:
        """
        # filtered_incomes = self.items[:]
        #
        # if date_filter:
        #     filtered_incomes = self.filter_by_date(filtered_incomes, date_filter)
        #
        # if from_filter and from_filter != "From":
        #     filtered_incomes = [income for income in filtered_incomes if income[2] == from_filter]
        #
        # if sort_order:
        #     reverse = sort_order.split()[0] == "⬇"
        #     if sort_order != 'Sort':
        #
        #         if sort_order.split()[1] == "Amount":
        #             filtered_incomes.sort(key=lambda x: x[1], reverse=reverse)
        #         elif sort_order.split()[1] == "Time":
        #             filtered_incomes.sort(key=lambda x: datetime.strptime(x[3], '%Y-%m-%d'), reverse=reverse)

        return headers + self.items

    def delete_payment(self, autonumbered_id):
        """
        Delete an income by autonumbered ID
        :param autonumbered_id:
        :return:
        """
        self.delete_item(autonumbered_id, self.database.del_payment, self.database.get_payments)


    # def filter_by_date(self, payments, date_filter):
    #     """
    #     Filter incomes by date
    #     :param pay:
    #     :param date_filter:
    #     :return:
    #     """
    #     if date_filter == "This month":
    #         start_date = datetime.now().replace(day=1)
    #     elif date_filter == "This year":
    #         start_date = datetime.now().replace(month=1, day=1)
    #     else:
    #         return payments
    #
    #     return [payment for payment in payments if datetime.strptime(payment[3], '%Y-%m-%d') >= start_date]

    def update_user_payments(self, autonumbered_id: int, updated_payment) -> None:
        """
        Update an income by autonumbered ID
        :param autonumbered_id:
        :param updated_payment:
        :return:
        """
        self.update_item(autonumbered_id, updated_payment, self.database.update_payment, self.database.get_payments)

    def get_sum(self):
        return 0

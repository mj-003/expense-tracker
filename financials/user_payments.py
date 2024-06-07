from datetime import datetime, timedelta
from .user_finances import UserFinancials


class UserPayments(UserFinancials):
    def __init__(self, database, user):
        super().__init__(database, user)
        self.load_payments()
        self.headers = self.get_headers()

    def get_headers(self):
        """
        Get the headers for the payments
        :return:  headers, as a list of lists
        """
        return [['No.', f'Amount {self.currency}', 'Title', 'Date']]

    def load_payments(self):
        """
        Load payments from the database
        :return: None
        """
        self.load_items(self.database.get_payments)

    def add_payment(self, payment):
        """
        Add a payment to the database
        :param payment: payment to add
        :return: None
        """
        self.add_item(payment, self.database.add_payment, self.database.get_payments)

    def get_payment(self, autonumbered_id: int) -> None:
        """
        Get a payment by autonumbered ID
        :param autonumbered_id: autonumbered ID of the payment
        :return: payment from the database, or None if the ID is invalid
        """
        item_id = self.get_item_id(autonumbered_id, self.database.get_payments)
        if item_id:
            return self.database.get_payment(item_id)
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")
            return None

    def get_payments(self, date_filter=None, title_filter=None, sort_order=None) -> list:
        """
        Get payments from the database
        :param date_filter: date filter, default is None, might be "This month", "This year" or "Upcoming"
        :param title_filter: title filter, default is None
        :param sort_order: sort order, default is None, might be ascending or descending, for date or amount
        :return: filtered and sorted payments
        """
        filtered_payments = self.items[:]

        if date_filter:
            filtered_payments = self.filter_by_date(filtered_payments, date_filter)

        if title_filter and title_filter != "Title":
            filtered_payments = [payment for payment in filtered_payments if payment[2] == title_filter]

        if sort_order:
            filtered_payments = self.sort_items(items=filtered_payments, sort_order=sort_order, date_index=3)

        self.headers = self.get_headers()
        return self.headers + filtered_payments

    def delete_payment(self, autonumbered_id):
        """
        Delete a payment by autonumbered ID
        :param autonumbered_id: autonumbered ID of the payment
        :return: None
        """
        self.delete_item(autonumbered_id, self.database.del_payment, self.database.get_payments)

    def filter_by_date(self, payments, date_filter):
        """
        Filter payments by date
        :param payments: List of payments
        :param date_filter: Filter criteria as a string, might be "This month", "This year" or "Upcoming"
        :return: List of filtered payments
        """
        today = datetime.now()

        if date_filter == "This month":
            start_date = today.replace(day=1)
            end_date = None
        elif date_filter == "This year":
            start_date = today.replace(month=1, day=1)
            end_date = None
        elif date_filter == "Upcoming":
            start_date = today
            end_date = today + timedelta(days=7)  # get payments for the next 7 days
        else:
            return payments

        if end_date:
            return [payment for payment in payments if
                    start_date <= datetime.strptime(payment[3], '%Y-%m-%d') <= end_date]
        else:
            return [payment for payment in payments if datetime.strptime(payment[3], '%Y-%m-%d') >= start_date]

    def update_user_payments(self, autonumbered_id: int, updated_payment) -> None:
        """
        Update a income by autonumbered ID
        :param autonumbered_id: autonumbered ID of the payment
        :param updated_payment: updated payment
        :return: None
        """
        self.update_item(autonumbered_id, updated_payment, self.database.update_payment, self.database.get_payments)

    def get_sum(self) -> float:
        """
        Get the sum of all upcoming (3 days) payments
        :return: sum of all upcoming payments
        """
        # payment[1] - amount
        # payment[3] - date
        today = datetime.now()
        in_three_days = today + timedelta(days=3)
        return sum([payment[1] for payment in self.items if today <= datetime.strptime(payment[3], '%Y-%m-%d') <= in_three_days])



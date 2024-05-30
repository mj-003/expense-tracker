from datetime import datetime
from .user_finances import UserFinancials

headers = [['No.', 'Amount', 'From', 'Date']]


class UserIncomes(UserFinancials):
    def __init__(self, database, user):
        super().__init__(database, user)

    def load_income(self):
        self.load_items()

    def add_income(self, income):
        self.add_item(income, self.database.add_income)

    def get_income(self, autonumbered_id):
        self.get_item(autonumbered_id, self.database.get_income)

    def delete_income(self, autonumbered_id):
        self.delete_item(autonumbered_id, self.database.del_income)

    def update_user_income(self, autonumbered_id, updated_income):
        self.update_item(autonumbered_id, updated_income, self.database.update_income)

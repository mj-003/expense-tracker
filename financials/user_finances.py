from abc import ABC, abstractmethod


# Abstract class for user financials
class UserFinancials(ABC):
    def __init__(self, database, user):
        self.database = database
        self.user = user
        self.items = []
        self.original_ids = []
        self.currency = user.currency

    def load_items(self, get_function):
        """
        Load items from the database
        :param get_function:
        :return:
        """
        user_id = self.database.get_user_id(self.user.username)
        items_from_db = get_function(user_id)
        self.items = []
        self.original_ids = []

        for idx, item in enumerate(items_from_db[::-1]):
            self.original_ids.append(item[0])
            autonumbered_item = [idx + 1] + list(item[2:])
            self.items.append(autonumbered_item)

    def add_item(self, item, add_function, get_function):
        """
        Add an item to the database
        :param item:
        :param add_function:
        :param get_function:
        :return:
        """
        add_function(self.user.id, item)
        self.load_items(get_function)

    def get_items(self, date_filter=None, category_filter=None, sort_order=None):
        pass

    def get_item(self, autonumbered_id, get_function):
        """
        Get an item by autonumbered ID
        :param autonumbered_id:
        :param get_function:
        :return:
        """
        if 0 < autonumbered_id <= len(self.original_ids):
            item_id = self.original_ids[autonumbered_id - 1]
            return get_function(item_id)
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")
            return None

    def delete_item(self, autonumbered_id, del_function, get_function):
        """
        Delete an item by autonumbered ID
        :param autonumbered_id:
        :param del_function:
        :param get_function:
        :return:
        """
        if 0 < autonumbered_id <= len(self.original_ids):
            expense_id = self.original_ids[autonumbered_id - 1]
            del_function(expense_id)
            self.load_items(get_function)
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")

    def update_item(self, autonumbered_id, updated_item, update_function, get_function):
        """
        Update an item by autonumbered ID
        :param autonumbered_id:
        :param updated_item:
        :param update_function:
        :param get_function:
        :return:
        """
        print(updated_item)
        if 0 < autonumbered_id <= len(self.original_ids):
            item_id = self.original_ids[autonumbered_id - 1]
            update_function(item_id, updated_item)
            self.load_items(get_function)
        else:
            print(f"Invalid autonumbered ID: {autonumbered_id}")

    @abstractmethod
    def get_sum(self):
        pass

    def update_currency(self, currency):
        self.currency = currency

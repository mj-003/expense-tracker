class Category:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def add_category(database, name):
        try:
            database.add_category(name)
        except ValueError as e:
            raise ValueError(str(e))

    @staticmethod
    def get_categories(database):
        return database.get_categories()

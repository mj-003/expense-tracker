from financials.user_expenses import UserExpenses
from utils.exports import export_to_excel, export_to_csv
from datetime import datetime


class HomePageController:
    def __init__(self, database, user, user_expenses: UserExpenses):
        self.user_expenses = user_expenses
        print('--------dupa dupa--------')
        print(user_expenses)

    def get_filtered_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        return self.user_expenses.get_expenses(date_filter, category_filter, sort_order)

    def get_filtered_items(self, items_list, date, category, sort):
        headers = [items_list[0]]
        print('jeaders: ',headers)
        filtered_items = items_list[1:]
        print('filtered_items: ', filtered_items)
        if date:
            if date == 'This month':
                date = datetime.now().replace(day=1)
                filtered_items = [item for item in items_list if datetime.strptime(item[3], '%Y-%m-%d') >= date]
            elif date == 'This year':
                date = datetime.now().replace(month=1, day=1)
                filtered_items = [item for item in items_list if datetime.strptime(item[3], '%Y-%m-%d') >= date]
        if category:
            if category == 'Expenses':
                filtered_items = [item for item in items_list if item[2] == 'Expense']
            if category == 'Incomes':
                filtered_items = [item for item in items_list if item[2] == 'Income']
        if sort:
            reverse = sort.split()[0] == "⬇"
            if sort != 'Sort':

                if sort.split()[1] == "Amount":
                    filtered_items.sort(key=lambda x: x[1], reverse=reverse)
                elif sort.split()[1] == "Time":
                    filtered_items.sort(key=lambda x: datetime.strptime(x[3], '%Y-%m-%d'), reverse=reverse)
        return headers + filtered_items

    def get_filtered_incomes(self, date, from_who, sort):
        pass





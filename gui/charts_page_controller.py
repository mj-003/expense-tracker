import datetime


class ChartPageController:
    def __init__(self, plotter, user_expenses, user_incomes):
        self.plotter = plotter
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        self.curr_month = datetime.datetime.now().replace(day=1)

    def show_chart(self, chart_function, month, year):
        if (chart_function == self.plotter.plot_category_pie_chart and
            self.check_if_available_month(month)) or (
                chart_function != self.plotter.plot_category_pie_chart and
                self.check_if_available(year)):
            fig, ax = chart_function(month=month, year=year)
            return fig, ax
        else:
            return None, None

    def show_prev_month(self):
        self.curr_month = (self.curr_month - datetime.timedelta(days=1)).replace(day=1)
        return self.curr_month.strftime('%Y-%m'), self.curr_month.year - 1

    def show_next_month(self):
        self.curr_month = (self.curr_month + datetime.timedelta(days=31)).replace(day=1)
        return self.curr_month.strftime('%Y-%m'), self.curr_month.year + 1

    def check_available_data(self, chart_function, month, year):
        if (chart_function == self.plotter.plot_category_pie_chart and
            self.check_if_available_month(month)) or (
                chart_function != self.plotter.plot_category_pie_chart and
                self.check_if_available(year)):
            return True
        else:
            return False

    def check_if_available(self, year):
        for item in self.user_expenses.get_expenses()[1:]:
            if item[4][:4] == str(year):
                return True
        for item in self.user_incomes.get_incomes()[1:]:
            if item[3][:4] == str(year):
                return True
        return False

    def check_if_available_month(self, month):
        for item in self.user_expenses.get_expenses()[1:]:
            if item[4][:7] == month:
                return True
        for item in self.user_incomes.get_incomes()[1:]:
            if item[3][:7] == month:
                return True
        return False

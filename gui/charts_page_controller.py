import datetime


class ChartPageController:
    """
    Controller for the Charts Page. This class is responsible
    for handling the logic for the charts page.
    """
    def __init__(self, plotter, user_expenses, user_incomes):
        self.plotter = plotter

        # Initialize the user_expenses and user_incomes
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes

        # Initialize the current month and year
        self.curr_month = datetime.datetime.now().replace(day=1)
        self.curr_year = self.curr_month.year

    def show_chart(self, chart_function, month, year):
        """
        Show a chart for the selected month and year
        :param chart_function: Function to plot the chart
        :param month: Month in the format 'YYYY-MM'
        :param year: Year in the format 'YYYY'
        :return: Figure and axis
        """
        if (chart_function == self.plotter.plot_category_pie_chart and
            self.check_if_available_month(month)) or (
                chart_function != self.plotter.plot_category_pie_chart and
                self.check_if_available(year)):
            fig, ax = chart_function(month=month, year=year)
            return fig, ax
        else:
            return None, None

    def show_prev_date(self):
        """
        Show the previous month and year
        :return: Previous month and year
        """
        self.curr_month = (self.curr_month - datetime.timedelta(days=1)).replace(day=1)
        self.curr_year = self.curr_year - 1
        return self.curr_month.strftime('%Y-%m'), self.curr_year

    def show_next_date(self):
        """
        Show the next month and year
        :return: Next month and year
        """
        self.curr_month = (self.curr_month + datetime.timedelta(days=31)).replace(day=1)
        self.curr_year = self.curr_year + 1
        return self.curr_month.strftime('%Y-%m'), self.curr_year

    def check_available_data(self, chart_function, month, year):
        """
        Check if data is available for the selected period
        :param chart_function: Function to plot the chart
        :param month: Month
        :param year: Year
        :return: True if data is available, False otherwise
        """
        if (chart_function == self.plotter.plot_category_pie_chart and
            self.check_if_available_month(month)) or (
                chart_function != self.plotter.plot_category_pie_chart and
                self.check_if_available(year)):
            return True
        else:
            return False

    def check_if_available(self, year):
        """
        Check if data is available for the selected year
        :param year: Year
        :return: True if data is available, False otherwise
        """
        expenses_found = False
        incomes_found = False

        # check expenses only if incomes are found
        for expense in self.user_expenses.get_expenses()[1:]:
            if expense[4][:4] == str(year):
                expenses_found = True
                break  #

        # check incomes only if expenses are found
        if expenses_found:
            for income in self.user_incomes.get_incomes()[1:]:
                if income[3][:4] == str(year):
                    incomes_found = True
                    break

        # return True if both expenses and incomes are found
        return expenses_found and incomes_found

    def check_if_available_month(self, month):
        """
        Check if data is available for the selected month
        :param month:
        :return:
        """
        # item[4] is the date field for expenses
        # item[3] is the date field for incomes

        for item in self.user_expenses.get_expenses()[1:]:
            if item[4][:7] == month:
                return True
        for item in self.user_incomes.get_incomes()[1:]:
            if item[3][:7] == month:
                return True
        return False

    def reset_date(self):
        """
        Reset the current month and year
        :return:
        """
        self.curr_month = datetime.datetime.now().replace(day=1)
        self.curr_year = self.curr_month.year



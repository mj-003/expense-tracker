import datetime

import customtkinter as ctk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.items_controller import ItemsController
from plots import MyPlotter
from gui.widgets_and_buttons import *


class HomePage(CTkFrame):
    def __init__(self, parent, app, user, user_expenses, user_incomes):
        super().__init__(parent)

        # Initialize the app, parent, and user
        self.table = None
        self.app = app
        self.parent = parent
        self.user = user

        # Initialize the controller and plotter
        self.controller = ItemsController(user_expenses, user_incomes, self.user.currency)
        self.plotter = MyPlotter(user_expenses, user_incomes)

        # Initialize the current month and today
        self.current_month = datetime.datetime.now().replace(day=1)
        self.today = datetime.datetime.today().strftime('%a, %-d.%m')

        # Initialize the widgets
        self.is_chart = None
        self.selected_row = None
        self.table_frame = None
        self.var_show_chart = ctk.StringVar(value="on")

        # Initialize the user expenses and incomes
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes

        # Initialize the user expenses and incomes lists
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.user_incomes_list = self.user_incomes.get_incomes()
        self.user_items_list = self.controller.create_user_items_list()

        # Initialize the filters
        self.date_filter = None
        self.category_filter = None
        self.sort_filter = None

        # Create the widgets
        self.create_title_frame()
        self.create_metrics_frame()
        self.create_search_container()
        self.show_user_items()
        self.create_chart_panel()
        self.if_show_chart()

    def create_title_frame(self):
        """
        Create title frame
        :return:
        """
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(25, 0))

        title_label = get_title_label(my_master=title_frame, my_text=f"Hello {self.user.username}!")
        title_label.pack(anchor="nw", side="left")

        today_label = get_today_label(my_master=title_frame, my_text=self.today)
        today_label.pack(anchor='nw', side='right', pady=5)

    def create_metrics_frame(self):
        """
        Create metrics frame
        :return:
        """
        metrics_frame = CTkFrame(master=self, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(25, 0))

        total_sum_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=400, height=60, corner_radius=30)
        total_sum_metric.grid_propagate(False)
        total_sum_metric.pack(side="left")

        logistics_img_data = Image.open("images/money2.png")
        logistics_img = CTkImage(light_image=logistics_img_data, dark_image=logistics_img_data, size=(43, 43))

        img_label = CTkLabel(master=total_sum_metric, image=logistics_img, text="")
        img_label.grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        total_this_month = get_total_this_month_label(my_master=total_sum_metric,
                                                      my_text=f"Total balance this month: {self.user_incomes.get_sum() - self.user_expenses.get_sum():.2f} zł")
        total_this_month.grid(row=0, column=1, sticky="sw")

    def create_search_container(self):
        """
        Create search container
        :return:
        """
        search_container = CTkFrame(master=self, height=50)
        search_container.pack(fill="x", pady=(27, 0), padx=27)

        self.date_filter = get_date_combo_box(my_master=search_container, my_width=185)
        self.date_filter.pack(side="left", padx=(13, 0), pady=13)

        self.category_filter = get_items_combo_box(my_master=search_container, my_width=185)
        self.category_filter.pack(side="left", padx=(13, 0), pady=13)

        self.sort_filter = get_sort_combo_box(my_master=search_container, my_width=185)
        self.sort_filter.pack(side="left", padx=(13, 0), pady=13)

        check_button = get_check_button(my_master=search_container, on_command=self.get_filtered_items, my_width=30)
        check_button.pack(side="left", padx=(13, 0), pady=13)

        self.is_chart = CTkCheckBox(master=search_container, text="Chart", font=('Aptos', 15),
                                    variable=self.var_show_chart, onvalue="on", offvalue="off",
                                    command=self.if_show_chart, fg_color="#2A8C55", width=30, height=30,
                                    hover_color='#207244')
        self.is_chart.pack(pady=15)

    def show_user_items(self):
        """
        Show user items
        :return:
        """
        # 'show_user_items' from widgets_and_buttons, returns the table
        self.table = show_user_items(self.table_frame, self, self.user_items_list, self.table)

    def get_filtered_items(self):
        """
        Get filtered items
        :return:
        """
        self.user_items_list = self.controller.create_user_items_list()

        # Get the filters
        date = self.date_filter.get()
        category = self.category_filter.get()
        sort = self.sort_filter.get()

        self.user_items_list = self.controller.get_filtered_items(self.user_items_list, date, category, sort)

        # Remove all rows
        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        # Add new rows
        for row_data in self.user_items_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def if_show_chart(self):
        """
        If show chart
        :return:
        """
        if self.var_show_chart.get() == "on":
            self.info_panel.pack(expand=True, fill="both", pady=27, padx=(0, 27))
        else:
            self.info_panel.pack_forget()

    def create_chart_panel(self):
        """
        Create chart panel
        :return:
        """
        self.info_panel = CTkFrame(master=self, fg_color="#eeeeee", border_width=0, border_color="#2A8C55",
                                   corner_radius=10, width=200)
        self.info_panel.pack_forget()
        self.update_chart()

    def update_chart(self):
        """
        Update chart
        :return:
        """
        # Clear the panel
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        # Get the data
        month_str, self.user_incomes_list, self.user_expenses_list = self.controller.get_chart_data(self.current_month)
        fig, ax = self.plotter.plot_incomes_expenses_per_month(month_str)

        # Create the chart
        chart_canvas = FigureCanvasTkAgg(fig, master=self.info_panel)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        # Create the buttons
        button_frame = ctk.CTkFrame(master=self.info_panel, fg_color="transparent")
        button_frame.pack(side='bottom', pady=10)

        prev_button = ctk.CTkButton(master=button_frame, text="Previous", fg_color='#2A8C55', hover_color='#207244',
                                    command=self.show_prev_month)
        prev_button.pack(side='left', padx=5)

        next_button = ctk.CTkButton(master=button_frame, text="Next", fg_color='#2A8C55', hover_color='#207244',
                                    command=self.show_next_month)
        next_button.pack(side='right', padx=5)

    def show_prev_month(self):
        """
        Show the previous month
        :return:
        """
        # get the previous month
        prev_month = self.current_month - datetime.timedelta(days=1)
        prev_month = prev_month.replace(day=1)

        # check if the previous month is available
        if self.controller.check_if_available_month(prev_month.strftime('%Y-%m')):
            self.current_month = prev_month
            self.update_chart()

    def show_next_month(self):
        """
        Show the next month
        :return:
        """
        # Get the next month
        next_month = self.current_month + datetime.timedelta(days=31)
        next_month = next_month.replace(day=1)

        # check if the next month is available
        if self.controller.check_if_available_month(next_month.strftime('%Y-%m')):
            self.current_month = next_month
            self.update_chart()

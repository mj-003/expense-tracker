import datetime

import customtkinter as ctk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.home_page_controller import HomePageController
from plots import MyPlotter
from widgets_and_buttons import *


class HomePage(CTkFrame):
    def __init__(self, parent, app, user, user_expenses, user_incomes):
        super().__init__(parent)

        self.controller = HomePageController(user_expenses, user_incomes)
        self.plotter = MyPlotter(user_expenses, user_incomes)
        self.current_month = datetime.datetime.now().replace(day=1)
        self.today = datetime.datetime.today().strftime('%a, %-d.%m')

        self.app = app
        self.parent = parent
        self.user = user

        self.is_chart = None
        self.selected_row = None
        self.table_frame = None
        self.var_show_chart = ctk.StringVar(value="on")

        self.user_expenses = user_expenses
        self.user_incomes = user_incomes

        self.user_expenses_list = self.user_expenses.get_expenses()
        self.user_incomes_list = self.user_incomes.get_incomes()
        self.user_items_list = self.controller.create_user_items_list()

        self.date_filter = None
        self.category_filter = None
        self.sort_filter = None

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
        metrics_frame = CTkFrame(master=self, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(25, 0))

        total_sum_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=400, height=60, corner_radius=30)
        total_sum_metric.grid_propagate(False)
        total_sum_metric.pack(side="left")

        logistics_img_data = Image.open("images/money.png")
        logistics_img = CTkImage(light_image=logistics_img_data, dark_image=logistics_img_data, size=(43, 43))

        img_label = CTkLabel(master=total_sum_metric, image=logistics_img, text="")
        img_label.grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        total_this_month = get_total_this_month_label(my_master=total_sum_metric, my_text=f"Total balance this month: {self.user_incomes.get_sum()-self.user_expenses.get_sum():.2f} zł")
        total_this_month.grid(row=0, column=1, sticky="sw")

    def create_search_container(self):
        """
        Create search container
        :return:
        """
        search_container = CTkFrame(master=self, height=50, fg_color="#F0F0F0")
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
                                    command=self.if_show_chart, fg_color="#2A8C55", width=30, height=30)
        self.is_chart.pack(pady=15)

    def show_user_items(self):
        if self.table_frame is None:
            self.table_frame = CTkScrollableFrame(master=self, fg_color="transparent")
            self.table_frame.pack(expand=True, fill="both", padx=27, pady=21, side='left')

            self.table = CTkTable(master=self.table_frame,
                                  values=self.user_items_list,
                                  colors=["#E6E6E6", "#EEEEEE"],
                                  header_color="#2A8C55",
                                  hover_color="#B4B4B4")

            self.table.pack(expand=True, fill='both')

        else:
            indicates_to_remove = list(range(len(self.table.values)))
            self.table.delete_rows(indicates_to_remove)

            for row_data in self.user_items_list:
                if len(row_data) > 1:
                    row_data[1] = f"{row_data[1]} zł"
                self.table.add_row(row_data)

        if self.table.rows > 0:
            self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_filtered_items(self):
        self.user_items_list = self.controller.create_user_items_list()
        date = self.date_filter.get()
        category = self.category_filter.get()
        sort = self.sort_filter.get()

        self.user_items_list = self.controller.get_filtered_items(self.user_items_list, date, category, sort)

        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        for row_data in self.user_items_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def if_show_chart(self):
        if self.var_show_chart.get() == "on":
            self.info_panel.pack(expand=True, fill="both", pady=27, padx=(0, 27))
        else:
            self.info_panel.pack_forget()

    def create_chart_panel(self):
        self.info_panel = CTkFrame(master=self, fg_color="#eeeeee", border_width=0, border_color="#2A8C55",
                                       corner_radius=10, width=200)
        self.info_panel.pack_forget()
        self.update_chart()

    def update_chart(self):
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        month_str, self.user_incomes_list, self.user_expenses_list = self.controller.get_chart_data(self.current_month)
        fig, ax = self.plotter.plot_incomes_expenses_per_month(month_str, self.user_incomes_list,
                                                               self.user_expenses_list)

        chart_canvas = FigureCanvasTkAgg(fig, master=self.info_panel)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        button_frame = ctk.CTkFrame(master=self.info_panel, fg_color="transparent")
        button_frame.pack(side='bottom', pady=10)

        prev_button = ctk.CTkButton(master=button_frame, text="Previous", fg_color='#2A8C55',
                                    command=self.show_prev_month)
        prev_button.pack(side='left', padx=5)

        next_button = ctk.CTkButton(master=button_frame, text="Next", fg_color='#2A8C55', command=self.show_next_month)
        next_button.pack(side='right', padx=5)

    def show_prev_month(self):
        if self.controller.check_if_available_month(self.current_month):
            self.current_month = self.current_month - datetime.timedelta(days=1)
            self.current_month = self.current_month.replace(day=1)
            self.update_chart()

    def show_next_month(self):
        if self.controller.check_if_available_month(self.current_month):
            next_month = self.current_month + datetime.timedelta(days=31)
            self.current_month = next_month.replace(day=1)
            self.update_chart()

from customtkinter import *
from PIL import Image
from gui.add_expense import ExpensePage
from gui import const


class HomePage(CTkFrame):
    def __init__(self, parent, app, database, user):
        super().__init__(parent)

        self.app = app
        self.parent = parent
        self.user = user
        self.database = database

        self.create_title_frame()
        self.create_metrics_frame()
        self.create_search_container()

    def create_title_frame(self):
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(25, 0))

        CTkLabel(master=title_frame, text=f"Hello {self.user.username}!", font=("Arial Black", 25),
                 text_color="#2A8C55").pack(
            anchor="nw", side="left")

        CTkButton(master=title_frame, text="+ New Expense", width=205, font=("Arial Black", 15),
                  text_color="#fff", fg_color="#2A8C55", hover_color="#207244",
                  command=lambda: self.app.show_frame(ExpensePage)).pack(anchor="ne", side="right")

    def create_metrics_frame(self):
        metrics_frame = CTkFrame(master=self, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(36, 0))

        total_sum_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
        total_sum_metric.grid_propagate(False)
        total_sum_metric.pack(side="left")

        logistics_img_data = Image.open("images/logistics_icon.png")
        logistics_img = CTkImage(light_image=logistics_img_data, dark_image=logistics_img_data, size=(43, 43))

        CTkLabel(master=total_sum_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12, 5),
                                                                             pady=10)

        CTkLabel(master=total_sum_metric, text="Total sum:", text_color="#fff", font=("Arial Black", 14)).grid(row=0,
                                                                                                               column=1,
                                                                                                               sticky="sw")
        CTkLabel(master=total_sum_metric, text="1235,99 zł", text_color="#fff", font=("Arial Black", 14),
                 justify="left").grid(
            row=1, column=1, sticky="nw", pady=(0, 10))

        biggest_expense_metrics = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=205, height=60)
        biggest_expense_metrics.grid_propagate(False)
        biggest_expense_metrics.pack(side="left", expand=True, anchor="center")

        shipping_img_data = Image.open("images/shipping_icon.png")
        shipping_img = CTkImage(light_image=shipping_img_data, dark_image=shipping_img_data, size=(43, 43))

        CTkLabel(master=biggest_expense_metrics, image=shipping_img, text="").grid(row=0, column=0, rowspan=2,
                                                                                   padx=(12, 5),
                                                                                   pady=10)

        CTkLabel(master=biggest_expense_metrics, text="Biggest expense:", text_color="#fff",
                 font=("Arial Black", 14)).grid(row=0,
                                                column=1,
                                                sticky="sw")
        CTkLabel(master=biggest_expense_metrics, text="199,94 zł", text_color="#fff", font=("Arial Black", 14),
                 justify="left").grid(
            row=1, column=1, sticky="nw", pady=(0, 10))

        mean_expense_month = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=205, height=60)
        mean_expense_month.grid_propagate(False)
        mean_expense_month.pack(side="right")

        delivered_img_data = Image.open("images/delivered_icon.png")
        delivered_img = CTkImage(light_image=delivered_img_data, dark_image=delivered_img_data, size=(43, 43))

        CTkLabel(master=mean_expense_month, image=delivered_img, text="").grid(row=0, column=0, rowspan=2, padx=(12, 5),
                                                                               pady=10)

        CTkLabel(master=mean_expense_month, text="Mean per month:", text_color="#fff", font=("Arial Black", 14)).grid(
            row=0,
            column=1,
            sticky="sw")
        CTkLabel(master=mean_expense_month, text="1000 zł", text_color="#fff", font=("Arial Black", 14),
                 justify="left").grid(
            row=1, column=1, sticky="nw", pady=(0, 10))

    def create_search_container(self):
        search_container = CTkFrame(master=self, height=50, fg_color="#F0F0F0")
        search_container.pack(fill="x", pady=(45, 0), padx=27)

        CTkEntry(master=search_container, width=305, placeholder_text="Search Order", border_color="#2A8C55",
                 border_width=2).pack(side="left", padx=(13, 0), pady=15)

        CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent Order", "Least Recent Order"],
                    button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",
                    dropdown_hover_color="#207244", dropdown_fg_color="#2A8C55", dropdown_text_color="#fff").pack(
            side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125,
                    values=["Status", "Processing", "Confirmed", "Packing", "Shipping", "Delivered", "Cancelled"],
                    button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",
                    dropdown_hover_color="#207244", dropdown_fg_color="#2A8C55", dropdown_text_color="#fff").pack(
            side="left", padx=(13, 0), pady=15)

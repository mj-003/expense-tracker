from CTkTable import CTkTable
from customtkinter import *
from PIL import Image
import customtkinter as ctk

import category
from expenses.expense import Expense
from gui.add_expense import ExpensePage
from gui.export_page import ExportPage
from categories import Categories
from expenses.user_expenses import UserExpenses

import customtkinter as ctk
from CTkTable import CTkTable
from PIL import Image


class HomePage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses):
        super().__init__(parent)
        self.selected_row = None
        self.table_frame = None
        self.expense_id = None
        self.user_expenses = user_expenses
        self.app = app
        self.parent = parent
        self.user = user
        self.database = database
        self.user_expenses_list = self.user_expenses.get_expenses()

        self.create_title_frame()
        self.create_metrics_frame()
        self.create_search_container()
        self.create_info_panel()  # Dodane: Tworzenie panelu bocznego
        self.show_user_expenses()

    def create_title_frame(self):
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(
            anchor="n",
            fill="x",
            padx=27,
            pady=(25, 0))

        CTkLabel(master=title_frame,
                 text=f"Hello {self.user.username}!",
                 font=("Arial Black", 25),
                 text_color="#2A8C55").pack(
            anchor="nw",
            side="left")

        CTkButton(master=title_frame,
                  text="+ New Expense",
                  width=205,
                  font=("Arial Black", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=lambda: self.app.show_frame(ExpensePage)).pack(
            anchor="ne",
            side="right")

    def create_metrics_frame(self):
        metrics_frame = CTkFrame(master=self, fg_color="transparent")
        metrics_frame.pack(
            anchor="n",
            fill="x",
            padx=27,
            pady=(36, 0))

        total_sum_metric = CTkFrame(master=metrics_frame,
                                    fg_color="#2A8C55",
                                    width=200,
                                    height=60)

        total_sum_metric.grid_propagate(False)
        total_sum_metric.pack(side="left")

        logistics_img_data = Image.open("images/logistics_icon.png")
        logistics_img = CTkImage(light_image=logistics_img_data,
                                 dark_image=logistics_img_data,
                                 size=(43, 43))

        CTkLabel(master=total_sum_metric,
                 image=logistics_img,
                 text="").grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(12, 5),
            pady=10)

        CTkLabel(master=total_sum_metric,
                 text="Total sum:",
                 text_color="#fff",
                 font=("Arial Black", 14)).grid(
            row=0,
            column=1,
            sticky="sw")

        CTkLabel(master=total_sum_metric,
                 text="1235,99 zł",
                 text_color="#fff",
                 font=("Arial Black", 14),
                 justify="left").grid(
            row=1,
            column=1,
            sticky="nw",
            pady=(0, 10))

        biggest_expense_metrics = CTkFrame(master=metrics_frame,
                                           fg_color="#2A8C55",
                                           width=205,
                                           height=60)

        biggest_expense_metrics.grid_propagate(False)
        biggest_expense_metrics.pack(side="left",
                                     expand=True,
                                     anchor="center")

        shipping_img_data = Image.open("images/shipping_icon.png")
        shipping_img = CTkImage(light_image=shipping_img_data,
                                dark_image=shipping_img_data,
                                size=(43, 43))

        CTkLabel(master=biggest_expense_metrics,
                 image=shipping_img,
                 text="").grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(12, 5),
            pady=10)

        CTkLabel(master=biggest_expense_metrics,
                 text="Biggest expense:",
                 text_color="#fff",
                 font=("Arial Black", 14)).grid(row=0,
                                                column=1,
                                                sticky="sw")

        CTkLabel(master=biggest_expense_metrics,
                 text="199,94 zł",
                 text_color="#fff",
                 font=("Arial Black", 14),
                 justify="left").grid(
            row=1,
            column=1,
            sticky="nw",
            pady=(0, 10))

        mean_expense_month = CTkFrame(master=metrics_frame,
                                      fg_color="#2A8C55",
                                      width=205,
                                      height=60)

        mean_expense_month.grid_propagate(False)
        mean_expense_month.pack(side="right")

        delivered_img_data = Image.open("images/delivered_icon.png")
        delivered_img = CTkImage(light_image=delivered_img_data,
                                 dark_image=delivered_img_data,
                                 size=(43, 43))

        CTkLabel(master=mean_expense_month,
                 image=delivered_img,
                 text="").grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(12, 5),
            pady=10)

        CTkLabel(master=mean_expense_month,
                 text="Mean per month:",
                 text_color="#fff",
                 font=("Arial Black", 14)).grid(
            row=0,
            column=1,
            sticky="sw")

        CTkLabel(master=mean_expense_month,
                 text="1000 zł",
                 text_color="#fff",
                 font=("Arial Black", 14),
                 justify="left").grid(
            row=1,
            column=1,
            sticky="nw",
            pady=(0, 10))

    def create_search_container(self):
        search_container = CTkFrame(master=self,
                                    height=50,
                                    fg_color="#F0F0F0")

        search_container.pack(fill="x",
                              pady=(45, 0),
                              padx=27)

        self.expense_id = CTkEntry(master=search_container,
                                   width=200,
                                   placeholder_text="More info (place ID)",
                                   border_color="#2A8C55",
                                   border_width=2, )
        self.expense_id.pack(
            side="left",
            padx=(13, 0),
            pady=15)

        CTkButton(master=search_container,
                  text='✔',
                  width=35,
                  font=("Arial", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_more_info).pack(
            side="left",
            padx=(13, 0),
            pady=15)

        CTkComboBox(master=search_container,
                    width=125,
                    values=["Date", "Most Recent Order", "Least Recent Order"],
                    button_color="#2A8C55",
                    border_color="#2A8C55",
                    border_width=2,
                    button_hover_color="#207244",
                    dropdown_hover_color="#207244",
                    dropdown_fg_color="#2A8C55",
                    dropdown_text_color="#fff").pack(
            side="left",
            padx=(13, 0),
            pady=15)

        CTkComboBox(master=search_container,
                    width=125,
                    values=['Category', Categories.TRANSPORT.value, Categories.FOOD.value,
                            Categories.ENTERTAINMENT.value,
                            Categories.HOME.value, Categories.PERSONAL.value, ],
                    button_color="#2A8C55",
                    border_color="#2A8C55",
                    border_width=2,
                    button_hover_color="#207244",
                    dropdown_hover_color="#207244",
                    dropdown_fg_color="#2A8C55",
                    dropdown_text_color="#fff").pack(
            side="left",
            padx=(13, 0),
            pady=15)

    def create_info_panel(self):
        self.info_panel = CTkFrame(master=self, fg_color="#2A8C55")
        self.info_panel.pack(expand=True, fill="both")
        self.info_panel.pack_forget()  # Ukrywanie panelu początkowo

    def show_user_expenses(self):
        if self.table_frame is None:
            # Tworzenie nowej ramki tabeli
            self.table_frame = CTkScrollableFrame(master=self, fg_color="transparent")
            self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)

            # Tworzenie nowej tabeli
            self.table = CTkTable(master=self.table_frame,
                                  values=self.user_expenses_list,
                                  colors=["#E6E6E6", "#EEEEEE"],
                                  header_color="#2A8C55",
                                  hover_color="#B4B4B4")
            self.table.pack(expand=True)

        # Aktualizacja istniejącej tabeli
        else:
            # Usuwanie wszystkich istniejących wierszy
            indicates_to_remove = list(range(len(self.table.values)))
            self.table.delete_rows(indicates_to_remove)

            # Dodawanie nowych wierszy
            for row_data in self.user_expenses_list:
                self.table.add_row(row_data)

            # Edytowanie pierwszego wiersza (zakładam, że chcesz to zrobić po każdej aktualizacji)
            if self.table.rows > 0:
                self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_more_info(self):
        self.selected_row = int(self.expense_id.get())
        expense_info = self.user_expenses_list[self.selected_row]
        print("Getting more info on row: ", self.selected_row)
        print(expense_info)

        # Wypełnianie panelu bocznego danymi
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        label = CTkLabel(self.info_panel, text=f"Expense Info (ID: {self.selected_row})", font=("Arial Black", 14),

                         width=30, height=2, text_color='white')
        label.pack(pady=(27, 27), padx=(27, 27), side='left')

        edit_button = CTkButton(self.info_panel, text="Edit", fg_color='white', text_color='black', width=70, height=50,
                                command=lambda: self.edit_expense(self.selected_row))
        edit_button.pack(side='right', padx=(10, 27), pady=10)

        delete_button = CTkButton(self.info_panel, text="Delete", fg_color='white', text_color='black', width=70,
                                  height=50, command=lambda: self.delete_expense(self.selected_row))
        delete_button.pack(side='right', padx=10, pady=10)

        photo_button = CTkButton(self.info_panel, text="Photo", fg_color='white', text_color='black', width=70,
                                 height=50, command=lambda: self.show_photo(self.selected_row))
        photo_button.pack(side='right', padx=10, pady=10)

        back_button = CTkButton(self.info_panel, text="Back", fg_color='white', text_color='black', width=70, height=50,
                                command=lambda: self.app.return_to_home_page())
        back_button.pack(side='right', padx=10, pady=10)

        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(27, 27))

    def edit_expense(self, row_id):
        expense_info = self.user_expenses_list[row_id]

        # Tworzenie okna do edycji wydatku
        edit_dialog = ctk.CTkToplevel(self)
        edit_dialog.title("Edit Expense")
        edit_dialog.geometry("400x300")  # Ustawienie rozmiaru okna

        # Etykiety i pola tekstowe w układzie grid

        ctk.CTkLabel(edit_dialog, text="Price:").grid(row=1, column=0, pady=10, padx=10, sticky="e")
        price_entry = ctk.CTkEntry(edit_dialog, textvariable=StringVar(value=expense_info[1]))
        price_entry.grid(row=1, column=1, pady=(20, 10), padx=10, sticky="w")

        ctk.CTkLabel(edit_dialog, text="Category:").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        category_entry = ctk.CTkEntry(edit_dialog, textvariable=StringVar(value=expense_info[2]))
        category_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        ctk.CTkLabel(edit_dialog, text="Date:").grid(row=3, column=0, pady=10, padx=10, sticky="e")
        date_entry = ctk.CTkEntry(edit_dialog, textvariable=StringVar(value=expense_info[3]))
        date_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        ctk.CTkLabel(edit_dialog, text="Recipe:").grid(row=4, column=0, pady=10, padx=10, sticky="e")
        photo_entry = ctk.CTkEntry(edit_dialog, textvariable=StringVar(value=expense_info[4]))
        photo_entry.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        save_button = ctk.CTkButton(edit_dialog, text="Save",
                                    fg_color="#2A8C55",
                                    command=lambda: self.save_expense(row_id, price_entry, category_entry, date_entry,
                                                                      photo_entry, edit_dialog))
        save_button.grid(row=5, column=0, columnspan=2, pady=20, padx=10)

        edit_dialog.columnconfigure(0, weight=1)
        edit_dialog.columnconfigure(1, weight=3)

    def save_expense(self, row_id, price_entry, category_entry, date_entry, photo_entry, edit_dialog):
        # Zapisanie zmienionych danych
        new_price = price_entry.get()
        new_category = category_entry.get()
        new_date = date_entry.get()
        new_photo = photo_entry.get()
        new_expense = Expense(new_price, new_category, new_date, new_photo)

        self.user_expenses.update_user_expense(row_id, new_expense)
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.show_user_expenses()
        edit_dialog.destroy()

    def delete_expense(self, row_id):
        # Usuwanie wydatku
        print(f"Deleting expense at row: {row_id}")
        self.user_expenses.delete_expense(row_id)
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.show_user_expenses()
        self.info_panel.pack_forget()  # Ukrywanie panelu po usunięciu wydatku

    def show_photo(self, selected_row):
        print('jkcahfjc')
        print(self.user_expenses.get_expense(self.selected_row))
        file_path = self.user_expenses.get_expense(self.selected_row)[6]

        if file_path:
            image = Image.open(file_path)
            image.show()

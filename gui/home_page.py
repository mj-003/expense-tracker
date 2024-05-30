import os
from tkinter import messagebox

import customtkinter as ctk
from CTkTable import CTkTable
from PIL import Image, ImageTk
from customtkinter import *

from categories import Categories
from financials.expense import Expense
from gui.add_expense import ExpensePage
from home_page_controller import HomePageController
from gui.add_income import IncomePage


class HomePage(CTkFrame):
    def __init__(self, parent, app, database, user, user_expenses, user_incomes):
        super().__init__(parent)
        self.selected_row = None
        self.table_frame = None
        self.expense_id = None
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        self.app = app
        self.parent = parent
        self.user = user
        self.database = database
        self.user_expenses_list = self.user_expenses.get_expenses()
        self.controller = HomePageController(database, user, user_expenses)

        self.date_filter = None
        self.category_filter = None
        self.sort_filter = None

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
                 font=("Aptos", 40, 'bold'),
                 text_color="#2A8C55").pack(
            anchor="nw",
            side="left")

        CTkButton(master=title_frame,
                  text="✚ New",
                  width=100,
                  height=50,
                  font=("Aptos", 16),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  corner_radius=50,
                  command=lambda: self.app.show_frame(ExpensePage)).pack(
            anchor="ne",
            side="right")

        CTkButton(master=title_frame,
                  text="✚ New",
                  width=100,
                  height=50,
                  font=("Aptos", 16),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  corner_radius=50,
                  command=lambda: self.app.show_frame(IncomePage)).pack(
            anchor="ne",
            side="right")

    def create_metrics_frame(self):
        metrics_frame = CTkFrame(master=self, fg_color="transparent")
        metrics_frame.pack(
            anchor="n",
            fill="x",
            padx=27,
            pady=(25, 0))



        total_sum_metric = CTkFrame(master=metrics_frame,
                                    fg_color="#2A8C55",
                                    width=350,
                                    height=60,
                                    corner_radius=30)

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
                 text="Total financials: 1929,99 zł",
                 text_color="#fff",
                 font=("Aptos", 18)).grid(
            row=0,
            column=1,
            sticky="sw")

        date_frame = CTkFrame(master=metrics_frame,
                              fg_color="transparent",
                              width=200,
                              height=60)

        date_frame.grid_propagate(False)
        date_frame.pack(side="right")

        CTkLabel(master=date_frame,
                 text="Thur, 30.05",
                 text_color="#2A8C55",
                 font=("Aptos", 35)).grid(
            row=0,
            column=1,
            sticky="se",
            pady=(0, 10))




    def create_search_container(self):
        search_container = CTkFrame(master=self,
                                    height=50,
                                    fg_color="#F0F0F0")

        search_container.pack(fill="x",
                              pady=(45, 0),
                              padx=27)

        self.expense_id = CTkEntry(master=search_container,
                                   width=110,
                                   placeholder_text="More (place ID)",
                                   border_color="#2A8C55",
                                   border_width=2, )
        self.expense_id.pack(
            side="left",
            padx=(13, 0),
            pady=15)

        CTkButton(master=search_container,
                  text='✔',
                  width=30,
                  font=("Aptos", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_more_info).pack(
            side="left",
            padx=(13, 0),
            pady=15)

        self.date_filter = CTkComboBox(master=search_container,
                                       width=120,
                                       values=["Date", "This month", "This year"],
                                       button_color="#2A8C55",
                                       border_color="#2A8C55",
                                       border_width=2,
                                       button_hover_color="#207244",
                                       dropdown_hover_color="#207244",
                                       dropdown_fg_color="#2A8C55",
                                       dropdown_text_color="#fff")

        self.date_filter.pack(
            side="left",
            padx=(13, 0),
            pady=15)

        self.category_filter = CTkComboBox(master=search_container,
                                           width=120,
                                           values=['Category', Categories.TRANSPORT.value, Categories.FOOD.value,
                                                   Categories.ENTERTAINMENT.value,
                                                   Categories.HOME.value, Categories.PERSONAL.value, ],
                                           button_color="#2A8C55",
                                           border_color="#2A8C55",
                                           border_width=2,
                                           button_hover_color="#207244",
                                           dropdown_hover_color="#207244",
                                           dropdown_fg_color="#2A8C55",
                                           dropdown_text_color="#fff")

        self.category_filter.pack(
            side="left",
            padx=(13, 0),
            pady=15)

        self.sort_filter = CTkComboBox(master=search_container,
                                       width=120,
                                       values=['Sort', '⬆ Amount', '⬇ Amount', '⬆ Time', '⬇ Time'],
                                       button_color="#2A8C55",
                                       border_color="#2A8C55",
                                       border_width=2,
                                       button_hover_color="#207244",
                                       dropdown_hover_color="#207244",
                                       dropdown_fg_color="#2A8C55",
                                       dropdown_text_color="#fff")

        self.sort_filter.pack(
            side="left",
            padx=(13, 0),
            pady=15)

        CTkButton(master=search_container,
                  text='✔',
                  width=30,
                  font=("Aptos", 15),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  command=self.get_filtered_expenses).pack(
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

        label = CTkLabel(self.info_panel, text=f"Expense Info (ID: {self.selected_row})", font=("Aptos", 14),

                         width=30, height=2, text_color='white')
        label.pack(pady=(27, 27), padx=(27, 27), side='left')

        edit_button = CTkButton(self.info_panel, text="📝", fg_color='white', text_color='black', width=60, height=60,
                                command=lambda: self.edit_expense(self.selected_row))
        edit_button.pack(side='right', padx=(10, 27), pady=10)

        delete_button = CTkButton(self.info_panel, text="✖️", fg_color='white', text_color='black', width=60,
                                  height=60, command=lambda: self.delete_expense(self.selected_row))
        delete_button.pack(side='right', padx=10, pady=10)

        photo_button = CTkButton(self.info_panel, text="📷", fg_color='white', text_color='black', width=60,
                                 height=60, command=lambda: self.show_photo())
        photo_button.pack(side='right', padx=10, pady=10)

        back_button = CTkButton(self.info_panel, text="🔙", fg_color='white', text_color='black', width=60, height=60,
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

    def show_photo(self):
        print(self.selected_row)
        print(self.user_expenses.get_expense(self.selected_row)[6])
        file_path = self.user_expenses.get_expense(self.selected_row)[6]
        print('dupsko')

        if file_path and os.path.exists(file_path):
            # Otwieranie nowego okna dialogowego
            photo_dialog = CTkToplevel(self)
            photo_dialog.title("Expense Photo")

            # Ładowanie i wyświetlanie obrazu w interfejsie
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)
            photo_label = CTkLabel(photo_dialog, image=photo)
            photo_label.image = photo  # Przechowujemy referencję do zdjęcia
            photo_label.pack(expand=True, fill='both', padx=20, pady=20)
        else:
            messagebox.showinfo("No photo", "No photo found for this expense")

    def get_filtered_expenses(self):
        date = self.date_filter.get()
        category = self.category_filter.get()
        sort = self.sort_filter.get()

        self.user_expenses_list = self.controller.get_filtered_expenses(date, category, sort)

        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        for row_data in self.user_expenses_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

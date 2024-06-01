from abc import ABC, abstractmethod
import os
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Style

import customtkinter as ctk
from CTkTable import CTkTable
from PIL import Image, ImageTk
from customtkinter import *
from tkcalendar import DateEntry, Calendar

from categories import Categories
from financials.expense import Expense
from gui.add_expense import ExpensePage
from item_page_controller import ItemPageController
from gui.add_income import IncomePage


class FinancialsPage(CTkFrame, ABC):
    def __init__(self, parent, app, database, user, user_items, user_items2):
        super().__init__(parent)
        # self.photo_path = None

        self.item_info = None
        self.edit_dialog = None
        self.search_container = None
        self.top = None
        self.date_entry = None
        self.calendar = None
        self.date_var = None
        self.new_item = None
        self.table = None
        self.info_panel = None
        self.financials = None
        self.selected_row = None
        self.table_frame = None
        self.item_id = None
        self.item_id_entry = None
        self.row_id = None

        self.user_items = user_items
        self.app = app
        self.parent = parent
        self.user = user
        self.database = database
        self.user_items_list = self.user_items.get_items()
        self.controller = ItemPageController(database, user, user_items, user_items)

        # dupa dupa dupa
        self.title = ''

        #self.create_title_frame()
        # self.create_metrics_frame()
        # self.create_search_container()
        # self.create_info_panel()
        # self.show_user_items()

    def create_title_frame(self, show_add_form_function):
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(
            anchor="n",
            fill="x",
            padx=27,
            pady=(25, 0))

        CTkLabel(master=title_frame,
                 text=f"Your {self.title}",
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
                  command=show_add_form_function).pack(
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
        self.search_container = CTkFrame(master=self,
                                    height=50,
                                    fg_color="#F0F0F0")

        self.search_container.pack(fill="x",
                              pady=(27, 0),
                              padx=27)

        self.row_id = CTkEntry(master=self.search_container,
                                   width=150,
                                   placeholder_text="More (place ID)",
                                   border_color="#2A8C55",
                                   border_width=2, )
        self.row_id.pack(
            side="left",
            padx=(13, 0),
            pady=15)
        #
        # CTkButton(master=search_container,
        #           text='✔',
        #           width=30,
        #           font=("Aptos", 15),
        #           text_color="#fff",
        #           fg_color="#2A8C55",
        #           hover_color="#207244",
        #           command=self.get_more_info).pack(
        #     side="left",
        #     padx=(13, 70),
        #     pady=15)
        #
        # self.date_filter = CTkComboBox(master=search_container,
        #                                width=130,
        #                                values=["Date", "This month", "This year"],
        #                                button_color="#2A8C55",
        #                                border_color="#2A8C55",
        #                                border_width=2,
        #                                button_hover_color="#207244",
        #                                dropdown_hover_color="#207244",
        #                                dropdown_fg_color="#2A8C55",
        #                                dropdown_text_color="#fff")
        #
        # self.date_filter.pack(
        #     side="left",
        #     padx=(13, 0),
        #     pady=15)
        #
        # self.category_filter = CTkComboBox(master=search_container,
        #                                    width=130,
        #                                    values=['Category', Categories.TRANSPORT.value, Categories.FOOD.value,
        #                                            Categories.ENTERTAINMENT.value,
        #                                            Categories.HOME.value, Categories.PERSONAL.value, ],
        #                                    button_color="#2A8C55",
        #                                    border_color="#2A8C55",
        #                                    border_width=2,
        #                                    button_hover_color="#207244",
        #                                    dropdown_hover_color="#207244",
        #                                    dropdown_fg_color="#2A8C55",
        #                                    dropdown_text_color="#fff")
        #
        # self.category_filter.pack(
        #     side="left",
        #     padx=(13, 0),
        #     pady=15)
        #
        # self.sort_filter = CTkComboBox(master=search_container,
        #                                width=130,
        #                                values=['Sort', '⬆ Amount', '⬇ Amount', '⬆ Time', '⬇ Time'],
        #                                button_color="#2A8C55",
        #                                border_color="#2A8C55",
        #                                border_width=2,
        #                                button_hover_color="#207244",
        #                                dropdown_hover_color="#207244",
        #                                dropdown_fg_color="#2A8C55",
        #                                dropdown_text_color="#fff")
        #
        # self.sort_filter.pack(
        #     side="left",
        #     padx=(13, 0),
        #     pady=15)
        #
        # CTkButton(master=search_container,
        #           text='✔',
        #           width=30,
        #           font=("Aptos", 15),
        #           text_color="#fff",
        #           fg_color="#2A8C55",
        #           hover_color="#207244",
        #           command=self.get_filtered_expenses).pack(
        #     side="left",
        #     padx=(13, 0),
        #     pady=15)

    def create_info_panel(self):
        self.info_panel = CTkFrame(master=self, fg_color="white", border_width=2, border_color="#2A8C55", width=200)
        self.info_panel.pack(expand=True, fill="both", pady=20)
        self.info_panel.pack_forget()

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
                self.table.add_row(row_data)

        if self.table.rows > 0:
            self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_more_info(self):
        self.row_id = int(self.row_id.get())
        print("Row ID: ", self.row_id)
        print("User items: ", self.user_items.get_items())
        item_info = self.user_items_list[self.row_id]
        print("Getting more info on row: ", self.row_id)
        print(item_info)

        for widget in self.info_panel.winfo_children():
            widget.destroy()

        label = CTkLabel(self.info_panel, text=f"{self.title} Info (ID: {self.row_id})", font=("Aptos", 14),
                         width=30, height=2, text_color='#2A8C55')
        label.pack(pady=(27, 27), padx=(27, 27), fill='both')

        edit_button = CTkButton(self.info_panel, text="✍︎", fg_color='#2A8C55', text_color='black',
                                corner_radius=100, width=40, height=60,
                                command=lambda: self.edit_item(self.row_id))
        edit_button.pack(padx=(10, 27), pady=10, fill='both')

        delete_button = CTkButton(self.info_panel, text="✕️", fg_color='#2A8C55', text_color='black',
                                  corner_radius=50, width=60,
                                  height=60, command=lambda: self.delete_item(self.row_id))
        delete_button.pack(padx=10, pady=10, fill='both')

        # photo_button = CTkButton(self.info_panel, text="📷", fg_color='#2A8C55', text_color='black',
        #                          corner_radius=50, width=60,
        #                          height=60, command=lambda: self.show_photo())
        # photo_button.pack(padx=10, pady=10, fill='both')

        back_button = CTkButton(self.info_panel, text="↩︎", font=('Aptos', 25), fg_color='#2A8C55',
                                text_color='white', corner_radius=50, width=60, height=60,
                                command=lambda: self.app.define_and_pack_frames())
        back_button.pack(padx=10, pady=10, fill='both')

        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def show_add_item_form(self):
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        label = CTkLabel(self.info_panel, text=f"Add New {self.title}", font=("Aptos", 18),
                         width=30, height=2, text_color='#2A8C55')
        label.pack(pady=(15, 10), padx=(27, 27))

        # price_entry = CTkEntry(self.info_panel, placeholder_text="Price")
        # price_entry.pack(pady=(10, 10), padx=(10, 10))
        #
        # category_entry = CTkComboBox(self.info_panel,
        #                              values=['Personal', 'Transport', 'Food', 'Entertainment', 'Home', 'Other'])
        # category_entry.pack(pady=(10, 10), padx=(10, 10))
        #
        # self.date_var = ctk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        # self.date_entry = ctk.CTkEntry(self.info_panel, textvariable=self.date_var, state='readonly',
        #                                fg_color="white")
        # self.date_entry.pack(pady=(10, 10), padx=(10, 10))
        # self.date_entry.bind("<Button-1>", self.open_calendar)
        #
        # payment_entry = CTkComboBox(self.info_panel, values=['Online', 'Card', 'Cash', 'Other'])
        # payment_entry.pack(pady=(10, 10), padx=(10, 10))
        #
        # CTkButton(master=self.info_panel,
        #           text="Photo",
        #           fg_color="white",
        #           hover_color="#207244",
        #           font=("Aptos", 12),
        #           border_color="#2A8C55",
        #           border_width=2,
        #           text_color="#2A8C55",
        #           text_color_disabled="white",
        #           command=self.upload_photo).pack(pady=(10, 10), padx=(10, 10))

        # save_button = CTkButton(self.info_panel, text="Save",
        #                         fg_color="#2A8C55",
        #                         command=lambda: self.save_new_item)
        # save_button.pack(pady=(10, 10), padx=(10, 10))
        #
        # self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def save_new_item(self):
        # new_price = price_entry.get()
        # new_category = category_entry.get()
        # new_date = self.date_entry.get()
        # new_payment = payment_entry.get()
        #
        # path = self.photo_path if self.photo_path else None
        # new_expense = Expense(amount=new_price, category=new_category, payment_method=new_payment, date=new_date,
        #                       photo_path=path)

        self.user_items.add_item(self.new_item)
        self.user_items_list = self.user_items.get_items()
        self.show_user_items()
        self.app.define_and_pack_frames()

    def edit_item(self):
        self.item_info = self.user_items.get_item()[self.row_id]

        self.edit_dialog = ctk.CTkToplevel(self)
        self.edit_dialog.title(f"Edit {self.title}")
        self.edit_dialog.geometry("400x300")

        # # ctk.CTkLabel(edit_dialog, text="Price:").grid(row=1, column=0, pady=10, padx=10, sticky="e")
        # # price_entry = ctk.CTkEntry(edit_dialog, textvariable=StringVar(value=expense_info[1]))
        # # price_entry.grid(row=1, column=1, pady=(20, 10), padx=10, sticky="w")
        # #
        # # ctk.CTkLabel(edit_dialog, text="Category:").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        # # category_entry = ctk.CTkEntry(edit_dialog, textvariable=StringVar(value=expense_info[2]))
        # # category_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        # #
        # # ctk.CTkLabel(edit_dialog, text="Date:").grid(row=3, column=0, pady=10, padx=10, sticky="e")
        # # date_entry = ctk.CTkEntry(edit_dialog, textvariable=StringVar(value=expense_info[3]))
        # # date_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        # #
        # # ctk.CTkLabel(edit_dialog, text="Payment method:").grid(row=4, column=0, pady=10, padx=10, sticky="e")
        # # payment_entry = ctk.CTkEntry(edit_dialog, textvariable=StringVar(value=expense_info[4]))
        # # payment_entry.grid(row=4, column=1, pady=10, padx=10, sticky="w")
        # #
        # # save_button = ctk.CTkButton(edit_dialog, text="Save",
        # #                             fg_color="#2A8C55",
        # #                             command=lambda: self.save_expense(row_id, price_entry, category_entry,
        # #                                                               date_entry,
        # #                                                               payment_entry, edit_dialog))
        # # save_button.grid(row=5, column=0, columnspan=2, pady=20, padx=10)
        #
        # edit_dialog.columnconfigure(0, weight=1)
        # edit_dialog.columnconfigure(1, weight=3)
        # # self.app.update_user_items(self.user_items)    ???

    def save_item(self, edit_dialog):
        self.save_new_item()
        edit_dialog.destroy()

    def delete_item(self):
        print(f"Deleting item at row: {self.row_id}")
        self.user_items.delete_item(self.row_id)
        self.user_items_list = self.user_items.get_items()
        self.show_user_items()
        self.info_panel.pack_forget()
        # self.app.update_user_items(self.user_expenses)

    # def show_photo(self):
    #     print(self.selected_row)
    #     print(self.user_expenses.get_expense(self.selected_row)[6])
    #     file_path = self.user_expenses.get_expense(self.selected_row)[6]
    #     print('dupsko')
    #
    #     if file_path and os.path.exists(file_path):
    #         photo_dialog = CTkToplevel(self)
    #         photo_dialog.title("Expense Photo")
    #
    #         image = Image.open(file_path)
    #         photo = ImageTk.PhotoImage(image)
    #         photo_label = CTkLabel(photo_dialog, image=photo)
    #         photo_label.image = photo
    #         photo_label.pack(expand=True, fill='both', padx=20, pady=20)
    #     else:
    #         messagebox.showinfo("No photo", "No photo found for this expense")

    def get_filtered_items(self):
        # date = self.date_filter.get()
        # category = self.category_filter.get()
        # sort = self.sort_filter.get()
        #
        # self.user_expenses_list = self.controller.get_filtered_expenses(date, category, sort)

        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        for row_data in self.user_items_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_user_items(self):
        return self.user_items

    # def upload_photo(self):
    #
    #     file_path = filedialog.askopenfilename(
    #         filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("Image Files", "*.jpeg"),
    #                    ("Image Files", "*.bmp")])
    #     if file_path:
    #         self.photo_path = file_path

    def open_calendar(self, event):
        if hasattr(self, 'top') and self.top.winfo_exists():
            self.top.lift()
            return

        # Create a top-level window for the calendar
        self.top = tk.Toplevel(self)
        self.top.geometry("+%d+%d" % (
            self.date_entry.winfo_rootx(), self.date_entry.winfo_rooty() + self.date_entry.winfo_height()))
        self.top.overrideredirect(True)  # Remove window decorations
        self.top.grab_set()
        self.top.lift()  # Bring the calendar window to the front

        self.calendar = Calendar(self.top, selectmode='day', date_pattern='yyyy-MM-dd')
        self.calendar.pack(pady=10, padx=10)
        select_button = ctk.CTkButton(self.top, text="Select", command=self.select_date)
        select_button.pack(pady=10)

    def select_date(self):
        self.date_var.set(self.calendar.get_date())
        self.top.destroy()

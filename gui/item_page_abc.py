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
from utils.entry_validators import validate_money


class FinancialsPage(CTkFrame, ABC):
    def __init__(self, parent, app, database, user, user_items, user_items2):
        super().__init__(parent)

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
        self.vcmd_money = (app.register(validate_money), '%P')


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
                                    width=400,
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
                 text=f"Total {self.title} this month: 1929,99 zł",
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
            print("User items: ", self.user_items_list)

            for row_data in self.user_items_list:
                self.table.add_row(row_data)

        if self.table.rows > 0:
            self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_more_info(self):

        for widget in self.info_panel.winfo_children():
            widget.destroy()

        label = CTkLabel(self.info_panel, text=f"{self.title} Info (ID: {self.selected_row})", font=("Aptos", 14),
                         width=30, height=2, text_color='#2A8C55')
        label.pack(pady=(27, 27), padx=(27, 27), fill='both')

        edit_button = CTkButton(self.info_panel, text="Edit", fg_color='#2A8C55', text_color='white', font=('Aptos', 12),
                                command=lambda: self.edit_item())

        edit_button.pack(padx=(15, 15), pady=10, fill='both')

        delete_button = CTkButton(self.info_panel, text="Delete", font=('Aptos', 12),fg_color='#2A8C55', text_color='white',
                                  command=lambda: self.delete_item())
        delete_button.pack(padx=15, pady=10, fill='both')

        back_button = CTkButton(self.info_panel, text="Back", font=('Aptos', 12), fg_color='#2A8C55',
                                text_color='white',
                                command=lambda: self.go_back())
        back_button.pack(padx=15, pady=15, fill='both', side='bottom')

        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def show_add_item_form(self):
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        label = CTkLabel(self.info_panel, text=f"Add New {self.title}", font=("Aptos", 18),
                         width=30, height=2, text_color='#2A8C55')
        label.pack(pady=(15, 10), padx=(27, 27))

    @abstractmethod
    def save_new_item(self):
        pass


    @abstractmethod
    def edit_item(self):
        pass

    def save_edited_item(self):
        self.save_new_item()
        self.edit_dialog.destroy()

    @abstractmethod
    def delete_item(self):
        pass

    def get_filtered_items(self):
        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        for row_data in self.user_items_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_user_items(self):
        return self.user_items

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

    def go_back(self):
        if self.edit_dialog:
            self.edit_dialog.destroy()
        self.info_panel.pack_forget()
        self.app.define_and_pack_frames()
        self.row_id.delete(0, 'end')



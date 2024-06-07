import tkinter as tk
from abc import ABC, abstractmethod
from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image
from tkcalendar import Calendar

from utils.entry_validators import validate_money, validate_more_info
from gui.widgets_and_buttons import *


class FinancialsPage(CTkFrame, ABC):
    def __init__(self, parent, app, user_items, currency):
        super().__init__(parent)

        # Initialize the app, parent, and user items
        self.app = app
        self.parent = parent

        # Initialize the frames
        self.description_window = None
        self.item_info = None
        self.edit_dialog = None
        self.search_container = None
        self.top = None
        self.table = None
        self.info_panel = None
        self.table_frame = None

        self.date_entry = None
        self.date_filter = None
        self.description = None
        self.calendar = None
        self.date_var = None
        self.new_item = None
        self.financials = None

        self.selected_row = None
        self.item_id = None
        self.item_id_entry = None
        self.row_id = None

        self.today = datetime.today().strftime('%a, %-d.%m')

        self.user_items = user_items
        self.user_items.update_currency(currency)
        self.user_items_list = self.user_items.get_items()

        self.title = ''
        self.vcmd_money = (app.register(validate_money), '%P')
        self.vcmd_more_info = (app.register(validate_more_info), '%d', '%P')
        self.today_sum = self.user_items.get_sum()

    def create_title_frame(self):
        """
        Create the title frame
        :return:
        """
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(25, 0))

        title = (CTkLabel(master=title_frame,
                          text=f"Your {self.title}",
                          font=("Aptos", 40, 'bold'),
                          text_color="#2A8C55"))
        title.pack(anchor="nw", side="left")

        today = (CTkLabel(master=title_frame,
                          text=self.today,
                          text_color="#2A8C55",
                          font=("Aptos", 35)))
        today.pack(anchor="ne", side="right")

    def create_metrics_frame(self, show_add_form_function, new_title):
        """
        Create the metrics frame
        :param show_add_form_function:
        :return:
        """
        metrics_frame = CTkFrame(master=self, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(25, 0))

        total_sum_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=420, height=60, corner_radius=30)
        total_sum_metric.grid_propagate(False)
        total_sum_metric.pack(side="left")

        logistics_img_data = Image.open("images/money2.png")
        logistics_img = CTkImage(light_image=logistics_img_data,
                                 dark_image=logistics_img_data,
                                 size=(43, 43))

        metric_label = (CTkLabel(master=total_sum_metric,
                                 image=logistics_img,
                                 text=""))
        metric_label.grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        sum_total = (CTkLabel(master=total_sum_metric,
                              text=new_title,
                              text_color="#fff",
                              font=("Aptos", 16)))
        sum_total.grid(row=0, column=1, sticky="sw")

        date_frame = CTkFrame(master=metrics_frame, fg_color="transparent", height=60)
        date_frame.grid_propagate(False)
        date_frame.pack(side="right")

        CTkButton(master=date_frame,
                  text="✚ New",
                  width=100,
                  height=60,
                  font=("Aptos", 16),
                  text_color="#fff",
                  fg_color="#2A8C55",
                  hover_color="#207244",
                  corner_radius=50,
                  command=show_add_form_function).pack(
            anchor="ne",
            side="right")

    def create_search_container(self, more_info_function):
        """
        Create the search container
        :param more_info_function:
        :return:
        """
        self.search_container = CTkFrame(master=self, height=50)
        self.search_container.pack(fill="x", pady=(27, 0), padx=27)

        self.row_id = CTkEntry(master=self.search_container,
                               width=150,
                               placeholder_text="More (place ID)",
                               border_color="#2A8C55",
                               border_width=1)
        self.row_id.pack(side="left", padx=(13, 0), pady=15)

        check_button = get_check_button(self.search_container, more_info_function, 30)
        check_button.pack(side="left", padx=(13, 0), pady=15)

    def create_info_panel(self):
        """
        Create the info panel
        :return:
        """
        self.info_panel = CTkFrame(master=self, border_width=0, border_color="#2A8C55", width=200)
        self.info_panel.pack(expand=True, fill="both", pady=20)
        self.info_panel.pack_forget()  # Hide the info panel

    def show_user_items(self):
        """
        Show the user items
        :return:
        """
        # 'show_user_items' is from gui/widgets_and_buttons.py. it returns the table
        self.table = show_user_items(self.table_frame, self, self.user_items_list, self.table)

    def validate_id(self, items):
        """
        Validate the ID
        :param items:
        :return:
        """
        if (not self.row_id.get().isdigit()) or int(self.row_id.get()) < 1 or int(self.row_id.get()) > len(
                items) - 1:  # -1 because of the header
            messagebox.showwarning("Warning", "Invalid ID.")
            return
        else:
            self.selected_row = int(self.row_id.get())
            self.item_info = items[self.selected_row]
            self.get_more_info()

    def get_more_info(self):
        """
        Get more info
        :return:
        """
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        label = CTkLabel(self.info_panel, text=f"{self.title} Info (ID: {self.selected_row})", font=("Aptos", 14),
                         width=30, height=2, text_color='#2A8C55')
        label.pack(pady=(27, 27), padx=(27, 27), fill='both')

        edit_button = CTkButton(self.info_panel, text="Edit", fg_color='#2A8C55', hover_color='#207244',
                                text_color='white',
                                font=('Aptos', 12),
                                command=lambda: self.edit_item())

        edit_button.pack(padx=(15, 15), pady=10, fill='both')

        description_button = CTkButton(self.info_panel, text="Description", fg_color='#2A8C55', hover_color='#207244',
                                       text_color='white',
                                       font=('Aptos', 12),
                                       command=lambda: self.show_description())

        description_button.pack(padx=(15, 15), pady=10, fill='both')

        delete_button = CTkButton(self.info_panel, text="Delete", font=('Aptos', 12), fg_color='#2A8C55',
                                  hover_color='#207244',
                                  text_color='white',
                                  command=lambda: self.delete_item())
        delete_button.pack(padx=15, pady=10, fill='both')

        back_button = CTkButton(self.info_panel, text="Back", font=('Aptos', 12), fg_color='#2A8C55',
                                hover_color='#207244',
                                text_color='white',
                                command=lambda: self.go_back())
        back_button.pack(padx=15, pady=15, fill='both', side='bottom')

        self.info_panel.pack(expand=True, fill="both", pady=(27, 27), padx=(0, 27))

    def show_add_item_form(self):
        """
        Show the add item form
        :return:
        """
        # Destroy the widgets in the info panel
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        self.label = CTkLabel(self.info_panel, text=f"Add New {self.title}", font=("Aptos", 18),
                              width=30, height=2, text_color='#2A8C55')
        self.label.pack(pady=(15, 10), padx=(27, 27))

    def save_edited_item(self):
        """
        Save the edited item
        :return:
        """
        self.label.config(text=f'Total {self.title} this month: {self.user_items.get_sum():.2f} zł')
        self.label.pack(pady=(15, 10), padx=(27, 27))

        self.save_new_item()
        self.edit_dialog.destroy()

    def get_filtered_items(self):
        """
        Get the filtered items
        :return:
        """
        indicates_to_remove = []
        for i in range(self.table.rows):
            indicates_to_remove.append(i)
        self.table.delete_rows(indicates_to_remove)

        for row_data in self.user_items_list:
            self.table.add_row(row_data)
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")

    def get_user_items(self):
        """
        Get the user items
        :return:
        """
        return self.user_items

    def open_calendar(self, event):
        """
        Open the calendar
        :param event:
        :return:
        """
        self.top = tk.Toplevel(self)
        self.top.geometry("+%d+%d" % (
            self.date_entry.winfo_rootx(), self.date_entry.winfo_rooty() + self.date_entry.winfo_height()))
        self.top.overrideredirect(True)
        self.top.grab_set()
        self.top.lift()

        self.calendar = Calendar(self.top, selectmode='day', date_pattern='yyyy-MM-dd')
        self.calendar.pack(pady=10, padx=10)
        select_button = ctk.CTkButton(self.top, text="Select", command=self.select_date, fg_color='#2A8C55')
        select_button.pack(pady=10)
        self.top.wait_window()

    def select_date(self):
        """
        Select the date
        :return:
        """
        self.date_var.set(self.calendar.get_date())
        self.top.grab_release()
        self.top.destroy()

    def go_back(self):
        """
        Go back
        :return:
        """
        # Destroy the widgets in the edit dialog
        if self.edit_dialog:
            self.edit_dialog.destroy()
        self.info_panel.pack_forget()
        self.row_id.delete(0, 'end')

    def add_buttons(self):
        """
        Add buttons
        :return:
        """
        save_button = get_check_button(self.info_panel, self.validate_and_save)
        save_button.pack(pady=(10, 10), padx=(35, 2), side='left')

        back_button = get_back_button(self.info_panel, self.go_back)
        back_button.pack(pady=(10, 10), padx=(2, 2), side='left')

        cancel_button = get_cancel_button(self.info_panel, self.cancel)
        cancel_button.pack(pady=(10, 10), padx=(2, 10), side='left')

    def add_description(self):
        """
        Add description
        :return:
        """
        self.description_window = tk.Toplevel(self.info_panel)
        self.description_window.title("Add Description")
        self.description_window.geometry("400x400")

        text = tk.Text(self.description_window, wrap="word", font=("Aptos", 12))
        text.pack(expand=True, fill="both", padx=10, pady=10)

        save_button = CTkButton(self.description_window, text="Save", fg_color='#2A8C55', hover_color='#207244',
                                command=lambda: self.save_description(text.get("1.0", "end")))
        save_button.pack(pady=(10, 10))

        self.description_window.focus_set()

    def save_description(self, description):
        """
        Save the description
        :param description:
        :return:
        """
        self.description = description.strip()  # Remove leading and trailing whitespaces
        self.description_window.destroy()

    def show_description(self):
        """
        Show the description
        :return:
        """
        description = self.get_description()

        if description is None:
            messagebox.showinfo("Description", "No description provided.")
        else:
            self.description_window = tk.Toplevel(self.info_panel)
            self.description_window.title("Description")
            self.description_window.geometry("400x300")

            text = tk.Text(self.description_window, wrap="word", font=("Aptos", 12))
            text.insert("1.0", description)
            text.pack(expand=True, fill="both")

    @abstractmethod
    def save_new_item(self):
        pass

    @abstractmethod
    def edit_item(self):
        pass

    @abstractmethod
    def delete_item(self):
        pass

    @abstractmethod
    def validate_and_save(self):
        pass

    @abstractmethod
    def cancel(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

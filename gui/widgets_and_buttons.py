from customtkinter import *

date_values = ['Date', 'This month', 'This year']
sort_values = ['Sort', '⬆ Amount', '⬇ Amount', '⬆ Time', '⬇ Time']
categories_values = ['Categories', 'Food', 'Transport', 'Entertainment', 'Home', 'Personal', 'Other']


def get_button(my_master, on_command: callable, my_text, my_width=30) -> CTkButton:
    return CTkButton(master=my_master,
                     text=my_text,
                     width=my_width,
                     font=("Aptos", 15),
                     text_color="#fff",
                     fg_color="#2A8C55",
                     hover_color="#207244",
                     command=on_command)


def get_check_button(my_master, on_command: callable, my_width=40) -> CTkButton:
    return get_button(my_master, on_command, "✔", my_width)


def get_cancel_button(my_master, on_command: callable, my_width=40) -> CTkButton:
    return get_button(my_master, on_command, "↩︎", my_width)


def get_back_button(my_master, on_command: callable, my_width=40) -> CTkButton:
    return get_button(my_master, on_command, "✗", my_width)


def get_combo_box(my_master, my_values: list, my_width: int = None) -> CTkComboBox:
    return CTkComboBox(master=my_master,
                       width=my_width,
                       values=my_values,
                       button_color="#2A8C55",
                       border_color="#2A8C55",
                       border_width=2,
                       button_hover_color="#207244",
                       dropdown_hover_color="#207244",
                       dropdown_fg_color="#2A8C55",
                       dropdown_text_color="#fff")


def get_entry(my_master, my_width: int, my_placeholder: str) -> CTkEntry:
    return CTkEntry(master=my_master,
                    width=my_width,
                    border_color="#2A8C55",
                    border_width=2,
                    placeholder_text=my_placeholder)


def get_date_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, date_values, my_width)


def get_sort_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, sort_values, my_width)


def get_categories_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, categories_values, my_width)

def get_how_often_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, ['How often', 'Daily', 'Weekly', 'Monthly', 'Yearly', 'Single'], my_width)


def get_upcoming_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, ['All', 'Upcoming', 'This month', 'This year'], my_width)


def get_validate_entry(my_master, my_width: int, my_placeholder: str, my_validate: str, my_validate_command: str,
                       my_text_variable) -> CTkEntry:
    return CTkEntry(master=my_master,
                    width=my_width,
                    placeholder_text=my_placeholder,
                    validate=my_validate,
                    validatecommand=my_validate_command,
                    textvariable=my_text_variable,
                    border_color="#2A8C55",
                    border_width=2)

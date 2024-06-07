from CTkTable import CTkTable
from customtkinter import *

date_values = ['Date', 'This month', 'This year']
sort_values = ['Sort', '⬆ Amount', '⬇ Amount', '⬆ Time', '⬇ Time']
categories_values = ['Categories', 'Food', 'Transport', 'Entertainment', 'Home', 'Personal', 'Other']
categories_no_title_values = ['Personal', 'Transport', 'Entertainment', 'Home', 'Food', 'Other']
items_values = ['Items', 'Incomes', 'Expenses']
payment_method_values = ['Online', 'Cash', 'Card', 'Other']
how_often_values = ['Once', 'Daily', 'Weekly', 'Monthly', 'Yearly']
upcoming_values = ['Upcoming', 'Today', 'Tomorrow', 'This week', 'This month']


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
                       border_width=1,
                       button_hover_color="#207244",
                       dropdown_hover_color="#207244",
                       dropdown_fg_color="#2A8C55",
                       dropdown_text_color="#fff")


def get_entry(my_master, my_width: int, my_placeholder: str) -> CTkEntry:
    return CTkEntry(master=my_master,
                    width=my_width,
                    border_color="#2A8C55",
                    border_width=1,
                    placeholder_text=my_placeholder)


def get_date_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, date_values, my_width)


def get_sort_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, sort_values, my_width)


def get_categories_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, categories_values, my_width)


def get_categories_no_title_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, categories_no_title_values, my_width)


def get_payment_method_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, payment_method_values, my_width)


def get_how_often_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, how_often_values, my_width)


def get_upcoming_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, upcoming_values, my_width)


def get_items_combo_box(my_master, my_width: int) -> CTkComboBox:
    return get_combo_box(my_master, items_values, my_width)


def show_user_items(table_frame, my_master, user_items_list, table):
    if table_frame is None:
        table_frame = CTkScrollableFrame(master=my_master, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21, side='left')

        table = CTkTable(master=table_frame,
                         values=user_items_list,
                         colors=["#E6E6E6", "#EEEEEE"],
                         header_color="#2A8C55",
                         hover_color="#B4B4B4")

        table.pack(expand=True, fill='both')

    else:
        indicates_to_remove = list(range(len(table.values)))
        table.delete_rows(indicates_to_remove)

        for row_data in user_items_list:
            if len(row_data) > 1:
                row_data[1] = f"{row_data[1]} zł"
            table.add_row(row_data)

    if table.rows > 0:
        table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
    return table


def get_validate_entry(my_master, my_width: int, my_placeholder: str, my_validate: str, my_validate_command: str,
                       my_text_variable) -> CTkEntry:
    return CTkEntry(master=my_master,
                    width=my_width,
                    placeholder_text=my_placeholder,
                    validate=my_validate,
                    validatecommand=my_validate_command,
                    textvariable=my_text_variable,
                    border_color="#2A8C55",
                    border_width=1)


def get_today_label(my_master, my_text: str) -> CTkLabel:
    return CTkLabel(master=my_master,
                    text=my_text,
                    font=("Aptos", 35),
                    text_color="#2A8C55")


def get_title_label(my_master, my_text: str) -> CTkLabel:
    return CTkLabel(master=my_master,
                    text=my_text,
                    font=("Aptos", 40, 'bold'),
                    text_color="#2A8C55")


def get_total_this_month_label(my_master, my_text: str) -> CTkLabel:
    return CTkLabel(master=my_master,
                    text=my_text,
                    font=("Aptos", 15),
                    text_color="#fff")

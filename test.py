import customtkinter as ctk
from tkinter import simpledialog

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.user_expenses_list = [
            ["1", "January", "1000"],
            ["2", "February", "1500"],
            ["3", "March", "1200"]
        ]

        self.show_user_expenses()

    def show_user_expenses(self):
        self.table_frame = ctk.CTkScrollableFrame(master=self, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        self.table = CTkTable(master=self.table_frame,
                              values=self.user_expenses_list,
                              colors=["#E6E6E6", "#EEEEEE"],
                              header_color="#2A8C55",
                              hover_color="#B4B4B4")
        self.table.pack(expand=True, fill="both")
        self.table.bind("<Button-1>", self.on_table_click)

    def on_table_click(self, event):
        row = self.table.get_row_clicked(event.x, event.y)
        print(row)
        if row is not None:
            self.show_edit_delete_options(row)

    def show_edit_delete_options(self, row):
        dialog = ctk.CTkToplevel(self)
        dialog.geometry("300x150")
        dialog.title("Edit or Delete")

        edit_button = ctk.CTkButton(dialog, text="Edit", command=lambda: self.edit_expense(row, dialog))
        edit_button.pack(pady=10)

        delete_button = ctk.CTkButton(dialog, text="Delete", command=lambda: self.delete_expense(row, dialog))
        delete_button.pack(pady=10)

    def edit_expense(self, row, dialog):
        new_value = simpledialog.askstring("Edit Expense", "Enter new expense:", initialvalue=self.user_expenses_list[row][2])
        if new_value:
            self.user_expenses_list[row][2] = new_value
            self.refresh_table()
        dialog.destroy()

    def delete_expense(self, row, dialog):
        del self.user_expenses_list[row]
        self.refresh_table()
        dialog.destroy()

    def refresh_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.show_user_expenses()

class CTkTable(ctk.CTkFrame):
    def __init__(self, master=None, values=None, colors=None, header_color=None, hover_color=None, **kwargs):
        super().__init__(master, **kwargs)
        self.values = values
        self.colors = colors
        self.header_color = header_color
        self.hover_color = hover_color
        self.create_table()

    def create_table(self):
        for i, (row_num, month, expense) in enumerate(self.values):
            bg_color = self.colors[i % len(self.colors)]
            row_label = ctk.CTkLabel(self, text=row_num, bg_color=bg_color)
            month_label = ctk.CTkLabel(self, text=month, bg_color=bg_color)
            expense_label = ctk.CTkLabel(self, text=expense, bg_color=bg_color)
            row_label.grid(row=i, column=0, sticky="nsew")
            month_label.grid(row=i, column=1, sticky="nsew")
            expense_label.grid(row=i, column=2, sticky="nsew")

            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def get_row_clicked(self, x, y):
        row_height = 25  # Adjust based on your row height
        row_index = y // row_height
        if row_index < len(self.values):
            return row_index
        return None

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

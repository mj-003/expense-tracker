import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime

class MyApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("CustomTkinter Date Entry")
        self.geometry("400x400")

        self.info_panel = ctk.CTkFrame(master=self, fg_color="white", border_width=2, border_color="#2A8C55", corner_radius=10, width=300)
        self.info_panel.pack(expand=True, fill="both", pady=20, padx=20)

        self.add_expense_form()

    def add_expense_form(self):
        for widget in self.info_panel.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(self.info_panel, text="Add New Expense", font=("Aptos", 18), width=30, height=2, text_color='#2A8C55')
        label.pack(pady=(15, 10), padx=(27, 27))

        price_entry = ctk.CTkEntry(self.info_panel, placeholder_text="Price")
        price_entry.pack(pady=(10, 10), padx=(10, 10))

        category_entry = ctk.CTkComboBox(self.info_panel, values=['Personal', 'Transport', 'Food', 'Entertainment', 'Home', 'Other'])
        category_entry.pack(pady=(10, 10), padx=(10, 10))

        # Add DateEntry with Calendar
        self.date_var = ctk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = ctk.CTkEntry(self.info_panel, textvariable=self.date_var, state='readonly')
        self.date_entry.pack(pady=(10, 10), padx=(10, 10))
        self.date_entry.bind("<Button-1>", self.open_calendar)

    def open_calendar(self, event):
        if hasattr(self, 'top') and self.top.winfo_exists():
            self.top.lift()
            return

        # Create a top-level window for the calendar
        self.top = tk.Toplevel(self)
        self.top.geometry("+%d+%d" % (self.date_entry.winfo_rootx(), self.date_entry.winfo_rooty() + self.date_entry.winfo_height()))
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

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

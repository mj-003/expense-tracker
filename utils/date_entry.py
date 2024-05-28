from tkinter import Toplevel, ttk

import customtkinter as ctk
from tkcalendar import Calendar


class DateEntry(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.date_var = ctk.StringVar()

        self.entry = ctk.CTkEntry(self,
                                  textvariable=self.date_var,
                                  fg_color="#F0F0F0",
                                  border_color="#2A8C55",
                                  width=200)

        self.entry.pack(side="left", padx=(10, 0), pady=10)

        self.button = ctk.CTkButton(self,
                                    text="▼",
                                    width=30,
                                    command=self.show_calendar,
                                    fg_color="#2A8C55",
                                    hover_color="#207244")

        self.button.pack(side="left", padx=(0, 10), pady=10)

        self.calendar_window = None

    def show_calendar(self):
        if self.calendar_window is not None:
            return

        self.calendar_window = Toplevel(self)
        self.calendar_window.withdraw()  # Hide window initially
        self.calendar_window.overrideredirect(True)  # Remove window decorations
        self.calendar_window.geometry("300x300")
        self.calendar_window.title("Select Date")

        # Position the calendar window below the entry field
        x = self.winfo_rootx() + self.entry.winfo_x()
        y = self.winfo_rooty() + self.entry.winfo_height() + 2
        self.calendar_window.geometry(f"300x300+{x}+{y}")

        style = ttk.Style(self.calendar_window)
        style.theme_use("default")

        cal = Calendar(self.calendar_window, selectmode='day', locale='en_US', disabledforeground='red',
                       cursor="hand2", background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                       selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        cal.pack(fill="both", expand=True, padx=10, pady=10)

        cal.bind("<<CalendarSelected>>", lambda e: self.set_date(cal.selection_get()))

        self.calendar_window.update_idletasks()  # Update window size and position
        self.calendar_window.deiconify()  # Show window

        self.calendar_window.protocol("WM_DELETE_WINDOW", self.close_calendar)
        self.calendar_window.bind("<FocusOut>", lambda e: self.close_calendar())  # Close calendar on focus out

    def set_date(self, date):
        self.date_var.set(date.strftime("%Y-%m-%d"))
        self.close_calendar()

    def close_calendar(self):
        if self.calendar_window is not None:
            self.calendar_window.destroy()
            self.calendar_window = None

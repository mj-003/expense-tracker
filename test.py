import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.widgets import DateEntry
import tkinter as tk

def on_date_selected(event):
    selected_date = date_entry.entry.get()
    Messagebox.show_info("Selected Date", f"You selected: {selected_date}")

# Tworzenie głównego okna aplikacji
root = ttk.Window(themename="flatly")
root.title("DateEntry Example")
root.geometry("300x200")

# Tworzenie stylu dla DateEntry
style = ttk.Style()
style.configure('TEntry', borderwidth=3, relief='solid', bordercolor='green', borderradius=10)

# Tworzenie widgetu DateEntry
date_entry = DateEntry(root, bootstyle=PRIMARY, dateformat="%Y-%m-%d", style='TEntry')
date_entry.pack(pady=20)
date_entry.bind("<<DateEntrySelected>>", on_date_selected)

# Uruchomienie pętli głównej
root.mainloop()

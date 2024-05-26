try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

from tkcalendar import DateEntry

style = ttk.Style()
style.theme_use('clam')  # -> uncomment this line if the styling does not work
style.configure('my.DateEntry',
                fieldbackground='light green',
                background='dark green',
                foreground='dark blue',
                arrowcolor='white')

dateentry = DateEntry(style='my.DateEntry')
dateentry.pack()

tk.mainloop()
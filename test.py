import tkinter as tk
from tkinter import ttk

def on_validate(P):
    if P == "":
        return True
    try:
        value = float(P)
        if len(P.split('.')[0]) > 5:
            return False
        if '.' in P and len(P.split('.')[1]) > 2:
            return False
        return True
    except ValueError:
        return False

root = tk.Tk()

vcmd = (root.register(on_validate), '%P')

money_entry = ttk.Entry(root, validate='key', validatecommand=vcmd)
money_entry.pack(pady=20, padx=20)

root.mainloop()

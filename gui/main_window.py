from tkinter import messagebox

import customtkinter as ctk

from database import Database
from gui.login_window import LoginWindow


class MainWindow:
    def __init__(self, master, user, database):
        self.master = master
        self.user = user
        self.database = database
        self.master.title("Śledzenie wydatków")
        self.master.geometry("600x400")

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.add_expense_button = ctk.CTkButton(self.frame, text="Dodaj wydatek", command=self.add_expense)
        self.add_expense_button.pack(pady=12, padx=10)

        self.show_stats_button = ctk.CTkButton(self.frame, text="Pokaż statystyki", command=self.show_stats)
        self.show_stats_button.pack(pady=12, padx=10)

        self.add_category_button = ctk.CTkButton(self.frame, text="Dodaj kategorię", command=self.add_category)
        self.add_category_button.pack(pady=12, padx=10)

    def add_expense(self):
        # logika dodawania wydatku
        pass

    def show_stats(self):
        # logika wyświetlania statystyk
        pass

    def add_category(self):
        new_category = ctk.CTkInputDialog(master=self.master, title="Dodaj kategorię", text="Nazwa kategorii:").get_input()
        if new_category:
            try:
                #Category.add_category(self.database, new_category)
                messagebox.showinfo("Sukces", "Kategoria dodana pomyślnie")
            except ValueError as e:
                messagebox.showerror("Błąd", str(e))

if __name__ == "__main__":
    database = Database()

    root = ctk.CTk()
    app = LoginWindow(root, database)
    root.mainloop()
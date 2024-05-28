from tkinter import filedialog
import tkinter as tk

def select_file():
    filename = filedialog.askopenfilename()
    path_entry.delete(0, 'end')  # Wyczyść aktualną zawartość pola tekstowego
    path_entry.insert(0, filename)  # Wstaw nową ścieżkę do pola tekstowego

root = tk.Tk()

# Utwórz pole tekstowe do wprowadzania ścieżki
path_entry = tk.Entry(root, width=50)
path_entry.pack(side="left", padx=10, pady=10)

# Utwórz przycisk do wyboru pliku
file_button = tk.Button(root, text="Wybierz plik", command=select_file)
file_button.pack(side="left", padx=10, pady=10)

root.mainloop()

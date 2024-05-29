import customtkinter

# Utwórz instancję aplikacji
app = customtkinter.CTk()
app.title("Edycja Wartości")

# Utwórz zmienną tekstową
initial_value = "Początkowa wartość"
text_var = customtkinter.StringVar(value=initial_value)

# Funkcja do aktualizacji wartości
def update_value():
    new_value = entry.get()
    text_var.set(new_value)
    print(text_var.get())

# Utwórz entry i button
entry = customtkinter.CTkEntry(app, textvariable=text_var)
entry.pack(padx=20, pady=10)

button = customtkinter.CTkButton(app, text="Zaktualizuj", command=update_value)
button.pack(padx=20, pady=10)

# Uruchom aplikację
app.mainloop()
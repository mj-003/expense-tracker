import customtkinter as ctk

class ColorChangeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Color Theme Changer")
        self.geometry("300x200")

        self.color_options = {
            "Dark": {"bg": "#333333", "fg": "#CCCCCC"},
            "Light": {"bg": "#EEEEEE", "fg": "#333333"},
            "Blue": {"bg": "#283747", "fg": "#D6DBDF"}
        }

        # Tworzenie przycisków do zmiany kolorów
        for color_name, colors in self.color_options.items():
            button = ctk.CTkButton(self, text=color_name, command=lambda c=colors: self.change_theme(c))
            button.pack(pady=10)

    def change_theme(self, colors):
        ctk.set_appearance_mode("System")  # System, Light, Dark
        ctk.set_default_color_theme("blue")  # blue, dark-blue, green
        # Zmiana kolorów tła i tekstu w całej aplikacji
        self.configure(bg=colors['bg'])  # Zmiana koloru tła
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=colors['bg'], hover_color=colors['fg'])

app = ColorChangeApp()
app.mainloop()

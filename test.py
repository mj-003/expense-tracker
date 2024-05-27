import customtkinter as ctk
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hover Image Example")
        self.geometry("800x600")

        self.user_expenses = [
            (1, '2024-05-27', 'Food', 100, 'Card', 'Lunch'),
            (2, '2024-05-26', 'Transport', 50, 'Cash', 'Bus ticket')
        ]

        self.icon = Image.open("gui/images/side-img.png")
        self.icon = self.icon.resize((100, 100), Image.ANTIALIAS)
        self.icon_image = ImageTk.PhotoImage(self.icon)

        self.create_table()

    def create_table(self):
        table_frame = ctk.CTkScrollableFrame(master=self, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        for i, expense in enumerate(self.user_expenses):
            row_frame = ctk.CTkFrame(master=table_frame)
            row_frame.pack(fill="x", padx=5, pady=5)

            for j, value in enumerate(expense[1:]):
                label = ctk.CTkLabel(master=row_frame, text=str(value), anchor="w")
                label.grid(row=0, column=j, padx=5, pady=5)

            # Bind hover events
            row_frame.bind("<Enter>", lambda event, rf=row_frame: self.show_image(event, rf))
            row_frame.bind("<Leave>", lambda event, rf=row_frame: self.hide_image(event, rf))

    def show_image(self, event, row_frame):
        self.image_popup = ctk.CTkToplevel(self)
        self.image_popup.overrideredirect(True)  # Remove window decorations
        self.image_popup.geometry(f"+{event.x_root + 20}+{event.y_root + 20}")  # Position near cursor
        label = ctk.CTkLabel(master=self.image_popup, image=self.icon_image, text="")
        label.pack()

    def hide_image(self, event, row_frame):
        if hasattr(self, 'image_popup'):
            self.image_popup.destroy()
            del self.image_popup

if __name__ == "__main__":
    app = App()
    app.mainloop()

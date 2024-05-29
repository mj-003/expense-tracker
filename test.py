import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk

# Ustawienia dla CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ImageApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Viewer")
        self.geometry("800x600")

        # Przyciski i etykiety
        self.upload_button = ctk.CTkButton(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.save_button = ctk.CTkButton(self, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=20)

        self.image_label = ctk.CTkLabel(self, text="No image uploaded")
        self.image_label.pack(pady=20)

        self.image_path = None
        self.image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("Image Files", "*.jpeg"), ("Image Files", "*.bmp")])
        if file_path:
            self.image_path = file_path
            self.image = Image.open(file_path)

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if save_path:
                self.image.save(save_path)



if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()

from customtkinter import *
from PIL import Image
from gui.home_page import HomePage
from gui.add_expense import ExpensePage


class App(CTk):
    def __init__(self):
        super().__init__()

        # Setting up Initial Things
        self.title("Sample Tkinter Structuring")
        self.geometry("856x645")
        set_appearance_mode("light")
        self.resizable(True, True)
        # self.sp = None
        self.create_sidebar()

        # Creating the container for the main content
        container = CTkFrame(self)
        container.pack(side="right", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize Frames
        self.frames = {}
        self.HomePage = HomePage
        self.ExpensePage = ExpensePage

        # Defining Frames and Packing it
        for F in [HomePage, ExpensePage]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def create_sidebar(self):
        sidebar_frame = CTkFrame(master=self, fg_color="#2A8C55", width=176, height=650, corner_radius=0)
        sidebar_frame.pack_propagate(False)
        sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("logo.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(78, 85))

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        analytics_img_data = Image.open("analytics_icon.png")
        analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

        CTkButton(master=sidebar_frame, image=analytics_img, text="Analytics", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w",
                  command=lambda: self.show_frame(ExpensePage)).pack(anchor="center", ipady=5,
                                                                     pady=(60, 0))

        package_img_data = Image.open("package_icon.png")
        package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)

        CTkButton(master=sidebar_frame, image=package_img, text="Expenses", fg_color="#fff",
                  font=("Arial Bold", 14),
                  text_color="#2A8C55", hover_color="#eee", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

        list_img_data = Image.open("list_icon.png")
        list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
        CTkButton(master=sidebar_frame, image=list_img, text="Export", fg_color="transparent",
                  font=("Arial Bold", 14),
                  hover_color="#207244", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

        settings_img_data = Image.open("settings_icon.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="center", ipady=5,
                                                                                   pady=(16, 0))

        person_img_data = Image.open("person_icon.png")
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
        CTkButton(master=sidebar_frame, image=person_img, text="Account", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="s", ipady=5,
                                                                                   pady=(200, 0))

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()

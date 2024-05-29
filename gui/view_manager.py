from customtkinter import *
from PIL import Image

from gui import const
from gui.home_page import HomePage
from gui.add_expense import ExpensePage
from gui.login_page import LoginPage
from gui.export_page import ExportPage
from expenses.user_expenses import UserExpenses
from gui import const
from user import User
from database import Database
from charts_page import ChartsPage


class App(CTk):
    def __init__(self):
        super().__init__()

        # Setting up Initial Things
        self.sidebar_frame = None
        self.title("Expense Tracker")
        self.geometry("856x645")
        set_appearance_mode("light")
        self.resizable(True, True)
        self.create_sidebar()
        self.container = CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        self.HomePage = HomePage
        self.ExpensePage = ExpensePage
        self.LoginPage = LoginPage
        self.ExportPage = ExportPage
        self.ChartsPage = ChartsPage

        self.user = None
        self.database = Database('expenses.db')
        self.user_expenses = None

        # show login page
        self.LoginPage = LoginPage(self.container, self, self.database)
        self.LoginPage.grid(row=0, column=0, sticky="nsew")
        self.LoginPage.tkraise()

        # self.show_frame(LoginPage)

    def create_sidebar(self):
        print("Creating sidebar")
        self.sidebar_frame = CTkFrame(master=self, fg_color="#2A8C55", width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("images/logo.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(78, 85))

        CTkLabel(master=self.sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        analytics_img_data = Image.open("images/analytics_icon.png")
        analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

        CTkButton(master=self.sidebar_frame, image=analytics_img, text="Analytics", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w",
                  command=lambda: self.show_frame(ChartsPage)).pack(anchor="center", ipady=5,
                                                                     pady=(60, 0))

        package_img_data = Image.open("images/package_icon.png")
        package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)

        CTkButton(master=self.sidebar_frame, image=package_img, text="Expenses", fg_color="#fff",
                  font=("Arial Bold", 14),
                  text_color="#2A8C55", hover_color="#eee", anchor="w", command=lambda: self.show_frame(HomePage)).pack(
            anchor="center", ipady=5, pady=(16, 0))

        list_img_data = Image.open("images/list_icon.png")
        list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
        CTkButton(master=self.sidebar_frame, image=list_img, text="Export", fg_color="transparent",
                  font=("Arial Bold", 14),
                  hover_color="#207244", anchor="w", command=lambda: self.show_frame(ExportPage)).pack(anchor="center", ipady=5, pady=(16, 0))

        settings_img_data = Image.open("images/settings_icon.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        CTkButton(master=self.sidebar_frame, image=settings_img, text="Settings", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="center", ipady=5,
                                                                                   pady=(16, 0))

        person_img_data = Image.open("images/person_icon.png")
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
        CTkButton(master=self.sidebar_frame, image=person_img, text="Account", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="s", ipady=5,
                                                                                   pady=(200, 0))

    def show_frame(self, cont):
        print("Showing frame")
        frame = self.frames[cont]
        frame.tkraise()

    def return_to_home_page(self):
        self.define_and_pack_frames()
        self.show_frame(HomePage)

    def define_and_pack_frames(self):
        for F in [HomePage, ExpensePage, ExportPage, ChartsPage]:
            frame = F(self.container, self, self.database, self.user, self.user_expenses)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        print('done packing frames')

    def after_logged_in(self, user: User, user_expenses: UserExpenses):
        print("Logged in")
        print('user: ', user)
        print('user_expenses: ', user_expenses)
        # self.create_sidebar()
        self.user = user
        self.user_expenses = user_expenses
        # print(self.user.username)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.define_and_pack_frames()
        self.show_frame(HomePage)


if __name__ == "__main__":
    app = App()
    app.mainloop()

from PIL import Image
from customtkinter import *

from charts_page import ChartsPage
from database import Database
from financials.user_expenses import UserExpenses
from financials.user_incomes import UserIncomes
from gui.expenses_page import ExpensesPage
from gui.export_page import ExportPage
from gui.home_page import HomePage
from gui.home_page_controller import HomePageController
from gui.incomes_page import IncomesPage
from gui.login_page import LoginPage
from user import User


class App(CTk):
    def __init__(self):
        super().__init__()

        # Setting up Initial Things
        self.sidebar_frame = None
        self.title("Expense Tracker")
        self.geometry("1000x645")
        set_appearance_mode("dark")
        self.resizable(True, True)

        self.container = CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        # self.HomePage = HomePage
        # self.LoginPage = LoginPage
        # self.ExportPage = ExportPage
        # self.ChartsPage = ChartsPage
        # self.IncomesPageTest = IncomesPage
        # self.ExpensePageTest = ExpensesPage
        # self.LoginPage = LoginPage

        self.user = None
        self.database = Database('expenses.db')
        self.user_expenses = None
        self.user_incomes = None

        self.show_login_page()

        # show login page
        # self.LoginPage = LoginPage(self.container, self, self.database)
        # self.LoginPage.grid(row=0, column=0, sticky="nsew")
        # self.LoginPage.tkraise()

    def show_login_page(self):
        self.LoginPage = LoginPage(self.container, self, self.database)
        self.LoginPage.grid(row=0, column=0, sticky="nsew")
        self.LoginPage.tkraise()

    def create_sidebar(self):
        print("Creating sidebar")
        self.container.pack_forget()
        self.sidebar_frame = CTkFrame(master=self, fg_color="#2A8C55", width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("images/money.png")
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

        CTkButton(master=self.sidebar_frame, image=package_img, text="Financials", fg_color="#fff",
                  font=("Arial Bold", 14),
                  text_color="#2A8C55", hover_color="#eee", anchor="w", command=lambda: self.show_frame(HomePage)).pack(
            anchor="center", ipady=5, pady=(16, 0))

        list_img_data = Image.open("images/list_icon.png")
        list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)

        settings_img_data = Image.open("images/settings_icon.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        CTkButton(master=self.sidebar_frame, image=settings_img, text="Incomes", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w",
                  command=lambda: self.show_frame(IncomesPage)).pack(anchor="center", ipady=5,
                                                                     pady=(16, 0))

        CTkButton(master=self.sidebar_frame, image=settings_img, text="Expenses", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w",
                  command=lambda: self.show_frame(ExpensesPage)).pack(anchor="center", ipady=5,
                                                                      pady=(16, 0))

        CTkButton(master=self.sidebar_frame, image=list_img, text="Export", fg_color="transparent",
                  font=("Arial Bold", 14),
                  hover_color="#207244", anchor="w", command=lambda: self.show_frame(ExportPage)).pack(anchor="center",
                                                                                                       ipady=5,
                                                                                                       pady=(16, 0))
        CTkButton(master=self.sidebar_frame, image=list_img, text="Payments", fg_color="transparent",
                  font=("Arial Bold", 14),
                  hover_color="#207244", anchor="w", command=lambda: self.show_frame(ExportPage)).pack(anchor="center",
                                                                                                       ipady=5,
                                                                                                       pady=(16, 0))
        person_img_data = Image.open("images/person_icon.png")
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
        CTkButton(master=self.sidebar_frame, image=person_img, text="Log out", fg_color="transparent",
                  command=self.log_out(),
                  font=("Arial Bold", 14), hover_color="#207244", anchor="w").pack(anchor="s", ipady=5,
                                                                                   pady=(150, 5))
        self.container.pack(side="right", fill="both", expand=True)

    def return_to_home_page(self):
        # self.define_and_pack_frames()
        self.show_frame(HomePage)

    def define_and_pack_frames(self):

        for F in [HomePage, ExportPage, ChartsPage, ExpensesPage, IncomesPage]:
            frame = F(self.container, self, self.database, self.user, self.user_expenses, self.user_incomes)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove()

    def define_frame(self, frame_class):

        self.user_incomes.load_incomes()
        self.user_expenses.load_expenses()

        if frame_class == HomePage:
            frame = HomePage(self.container, self, self.user, self.user_expenses, self.user_incomes)
        elif frame_class == ExportPage:
            frame = ExportPage(self.container, self, self.database, self.user, self.user_expenses, self.user_incomes)
        elif frame_class == ChartsPage:
            frame = ChartsPage(self.container, self, self.user_expenses, self.user_incomes)
        elif frame_class == ExpensesPage:
            frame = ExpensesPage(self.container, self, self.user_expenses)
        elif frame_class == IncomesPage:
            frame = IncomesPage(self.container, self, self.user_incomes)
        return frame

    def show_frame(self, cont):
        frame = self.define_frame(cont)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()

    def after_logged_in(self, user: User):
        self.create_sidebar()
        self.user = user
        self.user_expenses = UserExpenses(self.database, self.user)
        self.user_incomes = UserIncomes(self.database, self.user)

        self.LoginPage.grid_remove()

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.show_frame(HomePage)

    def log_out(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()

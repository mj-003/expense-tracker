from PIL import Image
from customtkinter import *

from gui.charts_page import ChartsPage
from database import Database
from financials.user_expenses import UserExpenses
from financials.user_incomes import UserIncomes
from financials.user_payments import UserPayments
from gui.account_page import AccountPage
from gui.expenses_page import ExpensesPage
from gui.export_page import ExportPage
from gui.home_page import HomePage
from gui.incomes_page import IncomesPage
from gui.login_page import LoginPage
from gui.payments_page import PaymentsPage
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

        # Create the container
        self.container = CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        # Initialize the frames
        self.frames = {}

        # Initialize the user, database, expenses, incomes and payments
        self.user = None
        self.database = Database('expenses.db')
        self.user_expenses = None
        self.user_incomes = None
        self.user_payments = None

        self.show_login_page()

    def show_login_page(self):
        """
        Shows the login page
        :return: None
        """
        self.LoginPage = LoginPage(self.container, self, self.database)
        self.LoginPage.grid(row=0, column=0, sticky="nsew")
        self.LoginPage.tkraise()

    def create_sidebar(self):
        """
        Creates the sidebar with the navigation buttons (Analytics, Financials, Incomes, Expenses, Payments, Export, Account)
        :return: None
        """
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
                  font=('Aptos', 14, 'bold'), hover_color="#207244", anchor="w",
                  command=lambda: self.show_frame(ChartsPage)).pack(anchor="center", ipady=5,
                                                                    pady=(60, 0))

        package_img_data = Image.open("images/package_icon.png")
        package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)

        CTkButton(master=self.sidebar_frame, image=package_img, text="Financials", fg_color="#fff",
                  font=('Aptos', 14, 'bold'),
                  text_color="#2A8C55", hover_color="#eee", anchor="w", command=lambda: self.show_frame(HomePage)).pack(
            anchor="center", ipady=5, pady=(16, 0))

        list_img_data = Image.open("images/list_icon.png")
        list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)

        settings_img_data = Image.open("images/settings_icon.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        CTkButton(master=self.sidebar_frame, image=settings_img, text="Incomes", fg_color="transparent",
                  font=('Aptos', 14, 'bold'), hover_color="#207244", anchor="w",
                  command=lambda: self.show_frame(IncomesPage)).pack(anchor="center", ipady=5,
                                                                     pady=(16, 0))

        CTkButton(master=self.sidebar_frame, image=settings_img, text="Expenses", fg_color="transparent",
                  font=('Aptos', 14, 'bold'), hover_color="#207244", anchor="w",
                  command=lambda: self.show_frame(ExpensesPage)).pack(anchor="center", ipady=5,
                                                                      pady=(16, 0))

        CTkButton(master=self.sidebar_frame, image=settings_img, text="Payments", fg_color="transparent",
                  font=('Aptos', 14, 'bold'),
                  hover_color="#207244", anchor="w", command=lambda: self.show_frame(PaymentsPage)).pack(
            anchor="center",
            ipady=5,
            pady=(16, 0))

        CTkButton(master=self.sidebar_frame, image=list_img, text="Export", fg_color="transparent",
                  font=('Aptos', 14, 'bold'),
                  hover_color="#207244", anchor="w", command=lambda: self.show_frame(ExportPage)).pack(anchor="center",
                                                                                                       ipady=5,
                                                                                                       pady=(16, 0))

        person_img_data = Image.open("images/person_icon.png")
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
        CTkButton(master=self.sidebar_frame, image=person_img, text="Account", fg_color="transparent",
                  font=("Aptos", 14, 'bold'), hover_color="#207244", anchor="w",
                  command=lambda: self.show_frame(AccountPage), ).pack(anchor="s", ipady=5,
                                                                       pady=(100, 5))
        self.container.pack(side="right", fill="both", expand=True)

    def define_frame(self, frame_class):
        """
        Define the frame. Create and return the frame based on the class
        :param frame_class: class of the frame
        :return: instance of the frame
        """
        # Load the expenses, incomes and payments
        if self.user_expenses is not None:
            self.user_expenses.load_expenses()
        if self.user_incomes is not None:
            self.user_incomes.load_incomes()
        if self.user_payments is not None:
            self.user_payments.load_payments()

        # Define the frame
        if frame_class == HomePage:
            frame = HomePage(self.container, self, self.user, self.user_expenses, self.user_incomes)
        elif frame_class == ExportPage:
            frame = ExportPage(self.container, self, self.database, self.user, self.user_expenses, self.user_incomes)
        elif frame_class == ChartsPage:
            frame = ChartsPage(self.container, self, self.user_expenses, self.user_incomes)
        elif frame_class == ExpensesPage:
            frame = ExpensesPage(self.container, self, self.user_expenses, self.user.currency)
        elif frame_class == IncomesPage:
            frame = IncomesPage(self.container, self, self.user_incomes, self.user.currency)
        elif frame_class == PaymentsPage:
            frame = PaymentsPage(self.container, self, self.user_payments, self.user.currency)
        elif frame_class == AccountPage:
            frame = AccountPage(self.container, self, self.user)
        elif frame_class == LoginPage:
            frame = LoginPage(self.container, self, self.database)
        return frame

    def show_frame(self, cont):
        """
        Show the frame
        :param cont: the class of the frame to show
        :return: None
        """
        frame = self.define_frame(cont)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()

    def after_logged_in(self, user: User):
        """
        After the user has logged in, show the home page
        :param user: user that has logged in
        :return: None
        """
        self.create_sidebar()
        self.user = user
        self.user_expenses = UserExpenses(self.database, self.user)
        self.user_incomes = UserIncomes(self.database, self.user)
        self.user_payments = UserPayments(self.database, self.user)

        self.LoginPage.grid_remove()

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.show_frame(HomePage)

    def log_out(self):
        """
        Log out the user, show the login page
        :return: None
        """
        self.sidebar_frame.pack_forget()
        self.container.pack_forget()
        self.show_login_page()
        self.container.pack(side="right", fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()

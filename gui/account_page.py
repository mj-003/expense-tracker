import datetime

import customtkinter as ctk
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.home_page_controller import HomePageController
from plots import MyPlotter
from widgets_and_buttons import *


class AccountPage(CTkFrame):
    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.today = datetime.datetime.today().strftime('%a, %-d.%m')

        self.app = app
        self.parent = parent
        self.user = user

from abc import ABC, abstractmethod
import os
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Style

import customtkinter as ctk
from CTkTable import CTkTable
from PIL import Image, ImageTk
from customtkinter import *
from tkcalendar import DateEntry, Calendar

from categories import Categories
from financials.expense import Expense
from financials.user_expenses import UserExpenses
from financials.user_incomes import UserIncomes
from gui.add_expense import ExpensePage
from home_page_controller import HomePageController
from gui.add_income import IncomePage

class ItemPageController:
    def __init__(self, database, user, user_expenses: UserExpenses, user_incomes: UserIncomes):
        self.user_expenses = user_expenses
        self.user_incomes = user_incomes
        self.user = user
        self.database = database
    @abstractmethod
    def get_filtered_expenses(self, date_filter=None, category_filter=None, sort_order=None):
        pass

    @abstractmethod
    def get_filtered_items(self, items_list, date, category, sort):
        pass

    @abstractmethod
    def get_filtered_incomes(self, date, from_who, sort):
        pass


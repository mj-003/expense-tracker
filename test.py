import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import customtkinter as ctk


class MyApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_incomes_list = [
            [1, 10.0, '', '2024-05-01'], [2, 10.0, '', '2024-05-02'], [3, 15.0, '', '2024-05-03'],
            [4, 15.0, '', '2024-05-05'], [5, 30.0, '', '2024-05-06'], [6, 30.0, '', '2024-05-07'],
            [7, 50.0, '', '2024-05-08'], [8, 50.0, '', '2024-05-09'], [9, 50.0, '', '2024-05-09'],
            [10, 50.0, '', '2024-05-10']
        ]
        self.user_expenses_list = [
            [1, 10.0, '', '2024-05-01', '2024-05-31', ''], [2, 13.0, '', '2024-05-02', '2024-05-31', ''],
            [3, 13.0, '', '2024-05-03', '2024-05-31', ''], [4, 15.0, '', '2024-05-04', '2024-05-31', ''],
            [5, 15.0, '', '2024-05-05', '2024-05-31', ''], [6, 15.0, '', '2024-05-06', '2024-05-31', ''],
            [7, 14.0, '', '2024-05-07', '2024-05-31', ''], [8, 19.0, '', '2024-05-08', '2024-05-31', ''],
            [9, 19.0, '', '2024-05-09', '2024-05-31', ''], [10, 19.0, '', '2024-05-10', '2024-05-31', ''],
            [11, 11.0, '', '', '2024-05-31', '']
        ]
        self.create_chart_panel()

    def plot_incomes_expenses_per_month(self, month, incomes_list, expenses_list):
        incomes_pd = pd.DataFrame(incomes_list, columns=["ID", "Amount", "From", "Date"])
        expenses_pd = pd.DataFrame(expenses_list,
                                   columns=["ID", "Amount", "Category", "Payment method", "Date", "Photo path"])
        incomes_pd['Date'] = pd.to_datetime(incomes_pd['Date'])
        expenses_pd['Date'] = pd.to_datetime(expenses_pd['Date'])

        incomes_pd = incomes_pd[incomes_pd['Date'].dt.strftime('%Y-%m') == month]
        expenses_pd = expenses_pd[expenses_pd['Date'].dt.strftime('%Y-%m') == month]
        total_income = incomes_pd['Amount'].sum()
        total_expenses = expenses_pd['Amount'].sum()

        fig, ax = plt.subplots(figsize=(3, 6))

        # Set the background color to transparent
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        categories = ['Income', 'Expenses']
        amounts = [total_income, total_expenses]
        colors = ['blue', 'orange']

        # Plot the bars and add text
        bars = ax.bar(categories, amounts, color=colors, edgecolor='none')
        for i, amount in enumerate(amounts):
            ax.text(i, amount, f'{amount}', ha='center', va='bottom')

        # Remove the spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Set limits and labels
        ax.set_xlim(-0.5, len(categories) - 0.5)
        ax.set_ylim(0, max(amounts) * 1.1)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories)
        ax.set_xlabel('Category')
        ax.set_ylabel('Amount')
        ax.set_title('Total Income and Expenses for ' + month)

        return fig, ax

    def create_chart_panel(self):
        self.info_panel = ctk.CTkFrame(master=self, fg_color="white", border_width=2, border_color="#2A8C55",
                                       corner_radius=10, width=300)
        self.info_panel.pack(expand=True, fill="both", pady=20, padx=20)

        fig, ax = self.plot_incomes_expenses_per_month('2024-05', self.user_incomes_list[1:],
                                                       self.user_expenses_list[1:])

        chart_canvas = FigureCanvasTkAgg(fig, master=self.info_panel)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

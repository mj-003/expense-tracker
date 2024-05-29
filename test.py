import matplotlib.pyplot as plt

# Przykładowe dane
labels = ['Net tuition and fees', 'Self-supporting', 'Private gifts', 'Taxes', 'Loan repayment', 'Promotions', 'All other']
sizes = [21, 21, 4, 8, 16, 8, 21]
colors = ['#66b3ff', '#ff6666', '#ffcc99', '#99ff99', '#c2c2f0', '#ffb3e6', '#c4e17f']

# Tworzenie wykresu
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(sizes, colors=colors, autopct=lambda pct: f'{int(round(pct))}%', startangle=140, wedgeprops=dict(width=0.45), pctdistance=0.85)

# Dodawanie legendy
legend = ax.legend(wedges, labels, loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=3)

# Środek wykresu
ax.set(aspect="equal")

# Dodanie tekstu w środku wykresu
plt.text(0, 0, 'Expenses', ha='center', va='center', fontsize=12, fontweight='bold')

# Dostosowanie marginesów figury, aby przesunąć wykres w lewo
fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

# Wyświetlanie wykresu
plt.show()

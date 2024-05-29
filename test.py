import tkinter as tk
from tkinterweb import HtmlFrame
import plotly.graph_objects as go
import numpy as np

# Ustawienia wykresu
np.random.seed(1)
x = np.random.rand(100)
y = np.random.rand(100)

f = go.FigureWidget([go.Scatter(x=x, y=y, mode='markers')])

scatter = f.data[0]
colors = ['#a3a7e4'] * 100
scatter.marker.color = colors
scatter.marker.size = [10] * 100
f.layout.hovermode = 'closest'

def update_point(trace, points, selector):
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        with f.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s

scatter.on_click(update_point)

# Generowanie HTML dla wykresu
plot_html = f.to_html(full_html=False)

# Ustawienia tkinter
root = tk.Tk()
root.wm_title("Plotly w Tkinter")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

# Tworzenie HtmlFrame i osadzenie w nim wykresu
html_frame = HtmlFrame(frame)
html_frame.set_content(plot_html)
html_frame.pack(fill=tk.BOTH, expand=1)

# Funkcje przycisków
def quit_app():
    root.quit()
    root.destroy()

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack(side=tk.BOTTOM)

root.mainloop()

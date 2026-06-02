# =====================================================
# NORMAL DISTRIBUTION GUI
# Interactive Mean & Standard Deviation Controls
# =====================================================

# INSTALL:
# pip install matplotlib scipy numpy

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =====================================================
# WINDOW
# =====================================================

root = tk.Tk()
root.title("Normal Distribution Visualizer")
root.geometry("1200x700")

# =====================================================
# LEFT CONTROL PANEL
# =====================================================

control_frame = tk.Frame(root, padx=15, pady=15)
control_frame.pack(side=tk.LEFT, fill=tk.Y)

title = tk.Label(
    control_frame,
    text="Normal Distribution Controls",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

# =====================================================
# MEAN SLIDER
# =====================================================

tk.Label(
    control_frame,
    text="Mean (μ)",
    font=("Arial", 12)
).pack()

mean_var = tk.DoubleVar(value=70)

mean_slider = tk.Scale(
    control_frame,
    from_=0,
    to=100,
    resolution=1,
    orient=tk.HORIZONTAL,
    variable=mean_var,
    length=250
)

mean_slider.pack(pady=5)

# =====================================================
# STANDARD DEVIATION 1
# =====================================================

tk.Label(
    control_frame,
    text="Standard Deviation σ1",
    font=("Arial", 12)
).pack()

sigma1_var = tk.DoubleVar(value=5)

sigma1_slider = tk.Scale(
    control_frame,
    from_=1,
    to=30,
    resolution=1,
    orient=tk.HORIZONTAL,
    variable=sigma1_var,
    length=250
)

sigma1_slider.pack(pady=5)

# =====================================================
# STANDARD DEVIATION 2
# =====================================================

tk.Label(
    control_frame,
    text="Standard Deviation σ2",
    font=("Arial", 12)
).pack()

sigma2_var = tk.DoubleVar(value=10)

sigma2_slider = tk.Scale(
    control_frame,
    from_=1,
    to=30,
    resolution=1,
    orient=tk.HORIZONTAL,
    variable=sigma2_var,
    length=250
)

sigma2_slider.pack(pady=5)

# =====================================================
# STANDARD DEVIATION 3
# =====================================================

tk.Label(
    control_frame,
    text="Standard Deviation σ3",
    font=("Arial", 12)
).pack()

sigma3_var = tk.DoubleVar(value=20)

sigma3_slider = tk.Scale(
    control_frame,
    from_=1,
    to=30,
    resolution=1,
    orient=tk.HORIZONTAL,
    variable=sigma3_var,
    length=250
)

sigma3_slider.pack(pady=5)

# =====================================================
# GRAPH AREA
# =====================================================

graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(8, 6))

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# =====================================================
# UPDATE GRAPH FUNCTION
# =====================================================

def update_graph():

    ax.clear()

    # Get slider values
    mean = mean_var.get()

    sigma1 = sigma1_var.get()
    sigma2 = sigma2_var.get()
    sigma3 = sigma3_var.get()

    # X-axis values
    x = np.linspace(0, 100, 1000)

    # Calculate curves
    y1 = norm.pdf(x, mean, sigma1)
    y2 = norm.pdf(x, mean, sigma2)
    y3 = norm.pdf(x, mean, sigma3)

    # Plot curves
    ax.plot(x, y1, label=f"σ = {sigma1}")
    ax.plot(x, y2, label=f"σ = {sigma2}")
    ax.plot(x, y3, label=f"σ = {sigma3}")

    # Labels
    ax.set_title(
        f"Normal Distribution of Exam Scores\nMean (μ) = {mean}"
    )

    ax.set_xlabel("Exam Score")
    ax.set_ylabel("Probability Density")

    ax.legend()

    ax.grid(True)

    # Refresh graph
    canvas.draw()

# =====================================================
# UPDATE BUTTON
# =====================================================

update_button = ttk.Button(
    control_frame,
    text="Update Graph",
    command=update_graph
)

update_button.pack(pady=20)

# =====================================================
# INITIAL GRAPH
# =====================================================

update_graph()

# =====================================================
# RUN APP
# =====================================================

root.mainloop()
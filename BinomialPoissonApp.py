# =========================================================
# ADVANCED DISTRIBUTION VISUALIZER
# Bernoulli • Binomial • Poisson
# =========================================================
#
# INSTALL:
# pip install matplotlib scipy numpy
#
# RUN:
# python distribution_app.py
#
# =========================================================

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, poisson
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =========================================================
# WINDOW
# =========================================================

root = tk.Tk()
root.title("Probability Distribution Visualizer")
root.geometry("1350x750")

# =========================================================
# LEFT PANEL
# =========================================================

control_frame = tk.Frame(root, padx=15, pady=15)
control_frame.pack(side=tk.LEFT, fill=tk.Y)

title = tk.Label(
    control_frame,
    text="Distribution Visualizer",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

# =========================================================
# BINOMIAL SECTION
# =========================================================

binom_label = tk.Label(
    control_frame,
    text="Binomial Distribution",
    font=("Arial", 15, "bold")
)
binom_label.pack(pady=(20, 5))

# n
tk.Label(control_frame, text="n (number of trials)").pack()

n_var = tk.IntVar(value=20)

n_slider = tk.Scale(
    control_frame,
    from_=1,
    to=100,
    orient=tk.HORIZONTAL,
    variable=n_var,
    length=250
)
n_slider.pack()

# p
tk.Label(control_frame, text="p (probability of success)").pack()

p_var = tk.DoubleVar(value=0.5)

p_slider = tk.Scale(
    control_frame,
    from_=0.01,
    to=1.0,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    variable=p_var,
    length=250
)
p_slider.pack()

# =========================================================
# POISSON SECTION
# =========================================================

poisson_label = tk.Label(
    control_frame,
    text="Poisson Distribution",
    font=("Arial", 15, "bold")
)
poisson_label.pack(pady=(25, 5))

# lambda
tk.Label(control_frame, text="λ (average rate)").pack()

lambda_var = tk.DoubleVar(value=5)

lambda_slider = tk.Scale(
    control_frame,
    from_=0.1,
    to=30.0,
    resolution=0.1,
    orient=tk.HORIZONTAL,
    variable=lambda_var,
    length=250
)
lambda_slider.pack()

# =========================================================
# OUTPUT TEXT
# =========================================================

stats_text = tk.Text(
    control_frame,
    height=18,
    width=40,
    font=("Consolas", 10)
)

stats_text.pack(pady=20)

# =========================================================
# GRAPH AREA
# =========================================================

graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, axes = plt.subplots(2, 2, figsize=(11, 7))

ax1 = axes[0, 0]
ax2 = axes[0, 1]
ax3 = axes[1, 0]
ax4 = axes[1, 1]

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# =========================================================
# UPDATE FUNCTION
# =========================================================

def update_graphs():

    # Clear old graphs
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()

    stats_text.delete(1.0, tk.END)

    # =====================================================
    # BINOMIAL
    # =====================================================

    n = n_var.get()
    p = p_var.get()

    x_binom = np.arange(0, n + 1)
    y_binom = binom.pmf(x_binom, n, p)

    # Plot PMF
    ax1.bar(x_binom, y_binom)

    ax1.set_title(f"Binomial PMF\nn={n}, p={p:.2f}")
    ax1.set_xlabel("Successes")
    ax1.set_ylabel("Probability")

    # Random sample histogram
    samples_binom = np.random.binomial(n, p, 1000)

    ax2.hist(samples_binom, bins=20)

    ax2.set_title("Binomial Sample Histogram")
    ax2.set_xlabel("Observed Values")
    ax2.set_ylabel("Frequency")

    # Expected value and variance
    mean_binom = n * p
    var_binom = n * p * (1 - p)

    # =====================================================
    # POISSON
    # =====================================================

    lam = lambda_var.get()

    x_poisson = np.arange(0, int(lam * 3 + 15))
    y_poisson = poisson.pmf(x_poisson, lam)

    # PMF
    ax3.bar(x_poisson, y_poisson)

    ax3.set_title(f"Poisson PMF\nλ={lam:.1f}")
    ax3.set_xlabel("Events")
    ax3.set_ylabel("Probability")

    # Random samples
    samples_poisson = np.random.poisson(lam, 1000)

    ax4.hist(samples_poisson, bins=20)

    ax4.set_title("Poisson Sample Histogram")
    ax4.set_xlabel("Observed Values")
    ax4.set_ylabel("Frequency")

    # Expected value and variance
    mean_poisson = lam
    var_poisson = lam

    # Example probability
    probability_example = poisson.pmf(3, lam)

    # =====================================================
    # TEXT OUTPUT
    # =====================================================

    explanation = f"""
==============================
BINOMIAL DISTRIBUTION
==============================

Parameters:
n = {n}
p = {p:.2f}

Expected Value:
E(X) = np
= {mean_binom:.2f}

Variance:
Var(X) = np(1-p)
= {var_binom:.2f}

How parameters affect shape:

• Larger n:
  -> Wider distribution
  -> More bell-shaped

• p near 0:
  -> Graph leans LEFT

• p near 1:
  -> Graph leans RIGHT

• p near 0.5:
  -> Most symmetric

==============================
POISSON DISTRIBUTION
==============================

Parameter:
λ = {lam:.2f}

Expected Value:
E(X) = λ
= {mean_poisson:.2f}

Variance:
Var(X) = λ
= {var_poisson:.2f}

Example Probability:
P(X = 3)
= {probability_example:.4f}

How λ affects shape:

• Small λ:
  -> Peak near zero
  -> Strong right skew

• Medium λ:
  -> More spread out

• Large λ:
  -> Becomes bell-shaped
  -> Looks more Normal
"""

    stats_text.insert(tk.END, explanation)

    # Refresh
    fig.tight_layout()
    canvas.draw()

# =========================================================
# BUTTON
# =========================================================

update_button = ttk.Button(
    control_frame,
    text="Update Graphs",
    command=update_graphs
)

update_button.pack(pady=10)

# =========================================================
# INITIAL DRAW
# =========================================================

update_graphs()

# =========================================================
# RUN
# =========================================================

root.mainloop()
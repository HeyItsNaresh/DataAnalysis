# =========================================================
# DISTRIBUTION FITTING VISUALIZER (GUI)
# Parameter Estimation & Goodness of Fit
# =========================================================
#
# INSTALL:
# pip install matplotlib scipy numpy scikit-learn
#
# RUN:
# python distribution_fitting_gui.py
#
# =========================================================

import tkinter as tk
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import norm, expon, uniform
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sklearn.metrics import mean_squared_error

# =========================================================
# WINDOW
# =========================================================

root = tk.Tk()

root.title("Distribution Fitting Visualizer")

root.geometry("1550x900")

# =========================================================
# CONTROL PANEL
# =========================================================

control_frame = tk.Frame(root, padx=15, pady=15)

control_frame.pack(side=tk.LEFT, fill=tk.Y)

title = tk.Label(
    control_frame,
    text="Distribution Fitting",
    font=("Arial", 20, "bold")
)

title.pack(pady=10)

# =========================================================
# DATA GENERATION CONTROLS
# =========================================================

tk.Label(
    control_frame,
    text="Sample Size",
    font=("Arial", 12)
).pack()

sample_size_var = tk.IntVar(value=1000)

sample_slider = tk.Scale(
    control_frame,
    from_=100,
    to=5000,
    resolution=100,
    orient=tk.HORIZONTAL,
    variable=sample_size_var,
    length=250
)

sample_slider.pack()

# =========================================================
# TRUE DISTRIBUTION SELECTION
# =========================================================

tk.Label(
    control_frame,
    text="Generate Data From",
    font=("Arial", 12)
).pack(pady=(15, 5))

distribution_var = tk.StringVar(value="Normal")

distribution_dropdown = ttk.Combobox(
    control_frame,
    textvariable=distribution_var,
    values=["Normal", "Exponential", "Uniform"],
    state="readonly",
    width=20
)

distribution_dropdown.pack()

# =========================================================
# PARAMETER CONTROLS
# =========================================================

# Mean
tk.Label(control_frame, text="Mean μ").pack(pady=(15, 0))

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

mean_slider.pack()

# Standard deviation
tk.Label(control_frame, text="Standard Deviation σ").pack()

sigma_var = tk.DoubleVar(value=10)

sigma_slider = tk.Scale(
    control_frame,
    from_=1,
    to=30,
    resolution=1,
    orient=tk.HORIZONTAL,
    variable=sigma_var,
    length=250
)

sigma_slider.pack()

# Lambda
tk.Label(control_frame, text="Rate λ").pack()

lambda_var = tk.DoubleVar(value=1)

lambda_slider = tk.Scale(
    control_frame,
    from_=0.1,
    to=10,
    resolution=0.1,
    orient=tk.HORIZONTAL,
    variable=lambda_var,
    length=250
)

lambda_slider.pack()

# =========================================================
# OUTPUT TEXT
# =========================================================

output_text = tk.Text(
    control_frame,
    width=42,
    height=25,
    font=("Consolas", 10)
)

output_text.pack(pady=20)

# =========================================================
# GRAPH AREA
# =========================================================

graph_frame = tk.Frame(root)

graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(11, 7))

canvas = FigureCanvasTkAgg(fig, master=graph_frame)

canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# =========================================================
# UPDATE FUNCTION
# =========================================================

def update_graph():

    ax.clear()

    np.random.seed(42)

    sample_size = sample_size_var.get()

    selected_distribution = distribution_var.get()

    mu = mean_var.get()
    sigma = sigma_var.get()
    lam = lambda_var.get()

    # =====================================================
    # GENERATE DATA
    # =====================================================

    if selected_distribution == "Normal":

        data = np.random.normal(
            loc=mu,
            scale=sigma,
            size=sample_size
        )

    elif selected_distribution == "Exponential":

        data = np.random.exponential(
            scale=1 / lam,
            size=sample_size
        )

    elif selected_distribution == "Uniform":

        data = np.random.uniform(
            low=0,
            high=100,
            size=sample_size
        )

    # =====================================================
    # HISTOGRAM
    # =====================================================

    count, bins, _ = ax.hist(
        data,
        bins=30,
        density=True,
        alpha=0.5,
        label="Sample Data Histogram"
    )

    x = (bins[:-1] + bins[1:]) / 2

    # =====================================================
    # FIT NORMAL
    # =====================================================

    mu_fit, sigma_fit = norm.fit(data)

    normal_pdf = norm.pdf(x, mu_fit, sigma_fit)

    ax.plot(
        x,
        normal_pdf,
        linewidth=2,
        label="Normal Fit"
    )

    # =====================================================
    # FIT EXPONENTIAL
    # =====================================================

    loc_exp, scale_exp = expon.fit(data)

    exp_pdf = expon.pdf(x, loc_exp, scale_exp)

    ax.plot(
        x,
        exp_pdf,
        linewidth=2,
        label="Exponential Fit"
    )

    # =====================================================
    # FIT UNIFORM
    # =====================================================

    loc_uni, scale_uni = uniform.fit(data)

    uniform_pdf = uniform.pdf(x, loc_uni, scale_uni)

    ax.plot(
        x,
        uniform_pdf,
        linewidth=2,
        label="Uniform Fit"
    )

    # =====================================================
    # MSE CALCULATIONS
    # =====================================================

    mse_normal = mean_squared_error(count, normal_pdf)

    mse_exp = mean_squared_error(count, exp_pdf)

    mse_uniform = mean_squared_error(count, uniform_pdf)

    mse_values = {
        "Normal": mse_normal,
        "Exponential": mse_exp,
        "Uniform": mse_uniform
    }

    best_fit = min(mse_values, key=mse_values.get)

    # =====================================================
    # GRAPH SETTINGS
    # =====================================================

    ax.set_title(
        f"Distribution Fitting\nGenerated From: {selected_distribution}"
    )

    ax.set_xlabel("Value")

    ax.set_ylabel("Density")

    ax.legend()

    ax.grid(True)

    # =====================================================
    # TEXT OUTPUT
    # =====================================================

    output_text.delete(1.0, tk.END)

    sample_preview = np.round(data[:20], 2)

    explanation = f"""
=================================================
GENERATED SAMPLE DATA
=================================================

First 20 Values:

{sample_preview}

=================================================
PARAMETER ESTIMATION
=================================================

Normal Distribution Fit:
μ = {mu_fit:.4f}
σ = {sigma_fit:.4f}

Exponential Distribution Fit:
scale = {scale_exp:.4f}

Uniform Distribution Fit:
min = {loc_uni:.4f}
max = {(loc_uni + scale_uni):.4f}

=================================================
GOODNESS OF FIT (MSE)
=================================================

Normal MSE:
{mse_normal:.6f}

Exponential MSE:
{mse_exp:.6f}

Uniform MSE:
{mse_uniform:.6f}

=================================================
BEST FIT
=================================================

{best_fit}

The distribution with the LOWEST
MSE is considered the best fit.
"""

    output_text.insert(tk.END, explanation)

    canvas.draw()

# =========================================================
# BUTTON
# =========================================================

update_button = ttk.Button(
    control_frame,
    text="Generate & Fit Distributions",
    command=update_graph
)

update_button.pack(pady=10)

# =========================================================
# INITIAL DRAW
# =========================================================

update_graph()

# =========================================================
# RUN APP
# =========================================================

root.mainloop()
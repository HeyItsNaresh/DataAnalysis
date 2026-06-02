# ==========================================================
# CONTINUOUS DISTRIBUTIONS VISUALIZER
# Uniform • Normal • Exponential
# Deterministic version: graphs do NOT randomly change
# unless parameters change
# ==========================================================

# INSTALL:
# pip install matplotlib scipy numpy

import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, norm, expon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Continuous Distribution Visualizer")
        self.root.geometry("1450x850")

        self.create_variables()
        self.create_layout()
        self.update_graphs()

    def create_variables(self):
        self.uniform_a = tk.DoubleVar(value=0)
        self.uniform_b = tk.DoubleVar(value=50)

        self.normal_mu = tk.DoubleVar(value=70)
        self.normal_sigma = tk.DoubleVar(value=10)

        self.exp_lambda = tk.DoubleVar(value=1)

    def create_slider(self, parent, label, variable, min_value, max_value, resolution):
        tk.Label(parent, text=label).pack()

        slider = tk.Scale(
            parent,
            from_=min_value,
            to=max_value,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            variable=variable,
            length=260
        )

        slider.pack(pady=3)
        return slider

    def create_layout(self):
        self.control_frame = tk.Frame(self.root, padx=15, pady=15)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            self.control_frame,
            text="Continuous Distributions",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        tk.Label(
            self.control_frame,
            text="Uniform Distribution",
            font=("Arial", 14, "bold")
        ).pack(pady=(20, 5))

        self.create_slider(
            self.control_frame,
            "Minimum a",
            self.uniform_a,
            0,
            100,
            1
        )

        self.create_slider(
            self.control_frame,
            "Maximum b",
            self.uniform_b,
            1,
            150,
            1
        )

        tk.Label(
            self.control_frame,
            text="Normal Distribution",
            font=("Arial", 14, "bold")
        ).pack(pady=(25, 5))

        self.create_slider(
            self.control_frame,
            "Mean μ",
            self.normal_mu,
            0,
            100,
            1
        )

        self.create_slider(
            self.control_frame,
            "Standard Deviation σ",
            self.normal_sigma,
            1,
            30,
            0.5
        )

        tk.Label(
            self.control_frame,
            text="Exponential Distribution",
            font=("Arial", 14, "bold")
        ).pack(pady=(25, 5))

        self.create_slider(
            self.control_frame,
            "Rate λ",
            self.exp_lambda,
            0.1,
            20,
            0.1
        )

        self.output_text = tk.Text(
            self.control_frame,
            width=42,
            height=18,
            font=("Consolas", 10)
        )

        self.output_text.pack(pady=20)

        update_button = ttk.Button(
            self.control_frame,
            text="Update Graphs",
            command=self.update_graphs
        )

        update_button.pack(pady=10)

        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.axes = plt.subplots(3, 2, figsize=(12, 10))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_graphs(self):
        a = self.uniform_a.get()
        b = self.uniform_b.get()
        mu = self.normal_mu.get()
        sigma = self.normal_sigma.get()
        lam = self.exp_lambda.get()

        if b <= a:
            messagebox.showerror(
                "Invalid Uniform Parameters",
                "Maximum b must be greater than Minimum a."
            )
            return

        for row in self.axes:
            for ax in row:
                ax.clear()

        ax1, ax2 = self.axes[0]
        ax3, ax4 = self.axes[1]
        ax5, ax6 = self.axes[2]

        # ==================================================
        # UNIFORM DISTRIBUTION
        # Deterministic PDF, not random samples
        # ==================================================

        x_uniform = np.linspace(a - 10, b + 10, 1000)
        y_uniform = uniform.pdf(x_uniform, loc=a, scale=b - a)

        ax1.plot(x_uniform, y_uniform)
        ax1.fill_between(x_uniform, y_uniform, alpha=0.3)

        ax1.set_title(f"Uniform PDF\n a={a}, b={b}")
        ax1.set_xlabel("x")
        ax1.set_ylabel("Density")

        uniform_mean = (a + b) / 2
        uniform_variance = ((b - a) ** 2) / 12

        ax2.plot(x_uniform, uniform.cdf(x_uniform, loc=a, scale=b - a))

        ax2.set_title("Uniform CDF")
        ax2.set_xlabel("x")
        ax2.set_ylabel("Cumulative Probability")

        # ==================================================
        # NORMAL DISTRIBUTION
        # Deterministic PDF and CDF
        # ==================================================

        x_normal = np.linspace(0, 100, 1000)

        normal_pdf = norm.pdf(x_normal, loc=mu, scale=sigma)
        normal_cdf = norm.cdf(x_normal, loc=mu, scale=sigma)

        ax3.plot(x_normal, normal_pdf)

        ax3.set_title(f"Normal PDF\n μ={mu}, σ={sigma}")
        ax3.set_xlabel("Exam Score")
        ax3.set_ylabel("Density")

        ax4.plot(x_normal, normal_cdf)

        ax4.set_title("Normal CDF")
        ax4.set_xlabel("Exam Score")
        ax4.set_ylabel("Cumulative Probability")

        normal_mean = mu
        normal_variance = sigma ** 2

        # ==================================================
        # EXPONENTIAL DISTRIBUTION
        # Deterministic PDF and CDF
        # ==================================================

        x_exp = np.linspace(0, 10, 1000)

        exp_pdf = expon.pdf(x_exp, scale=1 / lam)
        exp_cdf = expon.cdf(x_exp, scale=1 / lam)

        ax5.plot(x_exp, exp_pdf)

        ax5.set_title(f"Exponential PDF\n λ={lam}")
        ax5.set_xlabel("Waiting Time")
        ax5.set_ylabel("Density")

        ax6.plot(x_exp, exp_cdf)

        ax6.set_title("Exponential CDF")
        ax6.set_xlabel("Waiting Time")
        ax6.set_ylabel("Cumulative Probability")

        exp_mean = 1 / lam
        exp_variance = 1 / (lam ** 2)

        # ==================================================
        # TEXT OUTPUT
        # ==================================================

        self.output_text.delete("1.0", tk.END)

        explanation = f"""
========================================
UNIFORM DISTRIBUTION
========================================

a = {a}
b = {b}

Mean:
{uniform_mean:.4f}

Variance:
{uniform_variance:.4f}

Shape:
Flat because all values between
a and b are equally likely.

========================================
NORMAL DISTRIBUTION
========================================

Mean μ = {normal_mean}
Standard Deviation σ = {sigma}

Variance:
{normal_variance:.4f}

Shape:
Bell curve.

Increasing μ shifts the graph right.
Increasing σ makes it wider and flatter.

========================================
EXPONENTIAL DISTRIBUTION
========================================

Rate λ = {lam}

Mean:
{exp_mean:.4f}

Variance:
{exp_variance:.4f}

Shape:
Starts high and decreases.

Large λ means shorter waiting times.
Small λ means longer waiting times.
"""

        self.output_text.insert(tk.END, explanation)

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = DistributionApp(root)
    root.mainloop()
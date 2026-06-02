# ==========================================================
# ADVANCED STATISTICAL ANALYSIS APP
# ==========================================================
#
# FEATURES:
# ✔ Upload CSV Dataset
# ✔ Select Numeric Column
# ✔ Histogram
# ✔ Histogram + Normal Fit
# ✔ Professional QQ Plot
# ✔ Shapiro-Wilk Test
# ✔ Lilliefors Test
# ✔ Anderson-Darling Test
# ✔ Interpretation Table
#
# ==========================================================
# INSTALL:
#
# pip install pandas matplotlib scipy numpy statsmodels
#
# ==========================================================
# RUN:
#
# python stats_analysis_app.py
#
# ==========================================================

import tkinter as tk
from tkinter import filedialog, ttk, messagebox

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import scipy.stats as stats

from scipy.stats import norm
from scipy.stats import shapiro
from scipy.stats import anderson

from statsmodels.stats.diagnostic import lilliefors


# ==========================================================
# MAIN APPLICATION
# ==========================================================

class StatsAnalysisApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Advanced Statistical Analysis App")

        self.root.geometry("1450x850")

        self.df = None
        self.current_data = None

        # ==================================================
        # TOP CONTROLS
        # ==================================================

        top_frame = tk.Frame(root)

        top_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        upload_btn = tk.Button(
            top_frame,
            text="Upload CSV",
            font=("Arial", 12, "bold"),
            command=self.load_csv
        )

        upload_btn.pack(side="left", padx=5)

        self.column_combo = ttk.Combobox(
            top_frame,
            width=40,
            state="readonly"
        )

        self.column_combo.pack(side="left", padx=10)

        load_column_btn = tk.Button(
            top_frame,
            text="Load Column",
            font=("Arial", 12),
            command=self.load_column_data
        )

        load_column_btn.pack(side="left", padx=5)

        histogram_btn = tk.Button(
            top_frame,
            text="Histogram",
            font=("Arial", 12),
            command=self.plot_histogram
        )

        histogram_btn.pack(side="left", padx=5)

        fit_btn = tk.Button(
            top_frame,
            text="Add Normal Fit",
            font=("Arial", 12),
            command=self.plot_histogram_with_fit
        )

        fit_btn.pack(side="left", padx=5)

        qq_btn = tk.Button(
            top_frame,
            text="QQ Plot",
            font=("Arial", 12),
            command=self.plot_qq
        )

        qq_btn.pack(side="left", padx=5)

        tests_btn = tk.Button(
            top_frame,
            text="Run Normality Tests",
            font=("Arial", 12, "bold"),
            command=self.run_tests
        )

        tests_btn.pack(side="left", padx=5)

        # ==================================================
        # SAMPLE SIZE
        # ==================================================

        self.sample_size_label = tk.Label(
            root,
            text="Sample Size: N/A",
            font=("Arial", 12, "bold")
        )

        self.sample_size_label.pack(pady=5)

        # ==================================================
        # MAIN CONTENT AREA
        # ==================================================

        content_frame = tk.Frame(root)

        content_frame.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # GRAPH AREA
        # ==================================================

        self.graph_frame = tk.Frame(content_frame)

        self.graph_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # RIGHT PANEL
        # ==================================================

        right_frame = tk.Frame(
            content_frame,
            width=500
        )

        right_frame.pack(
            side="right",
            fill="y"
        )

        title_label = tk.Label(
            right_frame,
            text="Normality Test Results",
            font=("Arial", 16, "bold")
        )

        title_label.pack(pady=10)

        # ==================================================
        # TABLE
        # ==================================================

        columns = (
            "Test",
            "Statistic",
            "P-Value",
            "Interpretation"
        )

        self.tree = ttk.Treeview(
            right_frame,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:

            self.tree.heading(col, text=col)

            self.tree.column(
                col,
                width=150,
                anchor="center"
            )

        self.tree.pack(
            padx=10,
            pady=10,
            fill="both"
        )

        # ==================================================
        # INTERPRETATION GUIDE
        # ==================================================

        explanation_title = tk.Label(
            right_frame,
            text="Interpretation Guide",
            font=("Arial", 14, "bold")
        )

        explanation_title.pack(pady=5)

        explanation_text = tk.Text(
            right_frame,
            height=12,
            width=55,
            wrap="word"
        )

        explanation_text.pack(
            padx=10,
            pady=10
        )

        explanation = """
P > 0.05:
Fail to Reject Normality

P < 0.05:
Reject Normality

Shapiro-Wilk:
Most sensitive normality test.

Lilliefors:
Improved version of Kolmogorov-Smirnov.

Anderson-Darling:
Focuses heavily on distribution tails.

Large datasets make tests extremely sensitive.

Real-world datasets are rarely perfectly normal.
"""

        explanation_text.insert(
            tk.END,
            explanation
        )

        explanation_text.config(state="disabled")

    # ======================================================
    # LOAD CSV
    # ======================================================

    def load_csv(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )

        if not file_path:
            return

        try:

            self.df = pd.read_csv(file_path)

            numeric_columns = self.df.select_dtypes(
                include=np.number
            ).columns.tolist()

            self.column_combo["values"] = numeric_columns

            if numeric_columns:
                self.column_combo.current(0)

            messagebox.showinfo(
                "Success",
                "CSV Loaded Successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ======================================================
    # LOAD COLUMN
    # ======================================================

    def load_column_data(self):

        if self.df is None:
            return

        column = self.column_combo.get()

        self.current_data = self.df[column].dropna()

        sample_size = len(self.current_data)

        self.sample_size_label.config(
            text=f"Sample Size: {sample_size}"
        )

        messagebox.showinfo(
            "Loaded",
            f"{column} loaded successfully!"
        )

    # ======================================================
    # CLEAR GRAPH
    # ======================================================

    def clear_graph(self):

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    # ======================================================
    # HISTOGRAM
    # ======================================================

    def plot_histogram(self):

        if self.current_data is None:
            return

        self.clear_graph()

        fig, ax = plt.subplots(figsize=(9, 6))

        ax.hist(
            self.current_data,
            bins=20,
            density=True,
            alpha=0.75
        )

        ax.set_title(
            "Histogram",
            fontsize=16,
            fontweight="bold"
        )

        ax.set_xlabel("Values")
        ax.set_ylabel("Density")

        ax.grid(True, alpha=0.3)

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.graph_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ======================================================
    # HISTOGRAM + NORMAL FIT
    # ======================================================

    def plot_histogram_with_fit(self):

        if self.current_data is None:
            return

        self.clear_graph()

        fig, ax = plt.subplots(figsize=(9, 6))

        # Histogram

        ax.hist(
            self.current_data,
            bins=20,
            density=True,
            alpha=0.7,
            label="Data"
        )

        # Normal Fit

        mu, sigma = norm.fit(self.current_data)

        x = np.linspace(
            min(self.current_data),
            max(self.current_data),
            1000
        )

        y = norm.pdf(x, mu, sigma)

        ax.plot(
            x,
            y,
            linewidth=3,
            label="Normal Fit"
        )

        ax.set_title(
            f"Histogram + Normal Fit\nMean={mu:.2f}, Std={sigma:.2f}",
            fontsize=15,
            fontweight="bold"
        )

        ax.set_xlabel("Values")
        ax.set_ylabel("Density")

        ax.legend()

        ax.grid(True, alpha=0.3)

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.graph_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ======================================================
    # PROFESSIONAL QQ PLOT
    # ======================================================

    def plot_qq(self):

        if self.current_data is None:
            return

        self.clear_graph()

        data = np.array(self.current_data)

        # ==================================================
        # CREATE FIGURE
        # ==================================================

        fig, ax = plt.subplots(figsize=(9, 6))

        # ==================================================
        # SORT DATA
        # ==================================================

        sorted_data = np.sort(data)

        n = len(sorted_data)

        # ==================================================
        # THEORETICAL QUANTILES
        # ==================================================

        theoretical_quantiles = stats.norm.ppf(
            (np.arange(1, n + 1) - 0.5) / n
        )

        # ==================================================
        # FIT LINE
        # ==================================================

        slope, intercept = np.polyfit(
            theoretical_quantiles,
            sorted_data,
            1
        )

        fit_line = (
            slope * theoretical_quantiles
            + intercept
        )

        # ==================================================
        # CONFIDENCE BANDS
        # ==================================================

        residual_std = np.std(
            sorted_data - fit_line
        )

        upper_band = (
            fit_line + 1.96 * residual_std
        )

        lower_band = (
            fit_line - 1.96 * residual_std
        )

        # ==================================================
        # SCATTER POINTS
        # ==================================================

        ax.scatter(
            theoretical_quantiles,
            sorted_data,
            marker="+",
            s=70,
            label="Sample Quantiles"
        )

        # ==================================================
        # THEORETICAL LINE
        # ==================================================

        ax.plot(
            theoretical_quantiles,
            fit_line,
            linewidth=2,
            label="Theoretical Line"
        )

        # ==================================================
        # CONFIDENCE BANDS
        # ==================================================

        ax.plot(
            theoretical_quantiles,
            upper_band,
            linewidth=1,
            label="Upper Confidence Band"
        )

        ax.plot(
            theoretical_quantiles,
            lower_band,
            linewidth=1,
            label="Lower Confidence Band"
        )

        # ==================================================
        # CENTER AXES
        # ==================================================

        ax.axhline(
            0,
            linewidth=1
        )

        ax.axvline(
            0,
            linewidth=1
        )

        # ==================================================
        # TITLES
        # ==================================================

        ax.set_title(
            "Quantile-Quantile Plot",
            fontsize=18,
            fontweight="bold"
        )

        ax.set_xlabel(
            "Theoretical Quantiles",
            fontsize=14
        )

        ax.set_ylabel(
            "Sample Quantiles",
            fontsize=14
        )

        ax.legend()

        ax.grid(True, alpha=0.3)

        # ==================================================
        # SHOW INSIDE TKINTER
        # ==================================================

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.graph_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ======================================================
    # RUN NORMALITY TESTS
    # ======================================================

    def run_tests(self):

        if self.current_data is None:
            return

        # Clear previous rows

        for item in self.tree.get_children():
            self.tree.delete(item)

        data = self.current_data

        # ==================================================
        # SHAPIRO-WILK
        # ==================================================

        shapiro_stat, shapiro_p = shapiro(data)

        shapiro_result = (
            "Fail to Reject Normality"
            if shapiro_p > 0.05
            else "Reject Normality"
        )

        self.tree.insert(
            "",
            "end",
            values=(
                "Shapiro-Wilk",
                round(shapiro_stat, 5),
                f"{shapiro_p:.5f}",
                shapiro_result
            )
        )

        # ==================================================
        # LILLIEFORS
        # ==================================================

        lillie_stat, lillie_p = lilliefors(data)

        lillie_result = (
            "Fail to Reject Normality"
            if lillie_p > 0.05
            else "Reject Normality"
        )

        self.tree.insert(
            "",
            "end",
            values=(
                "Kolmogorov-Smirnov",
                round(lillie_stat, 5),
                f"{lillie_p:.5f}",
                lillie_result
            )
        )

        # ==================================================
        # ANDERSON-DARLING
        # ==================================================

        anderson_result = anderson(
            data,
            dist='norm'
        )

        ad_stat = anderson_result.statistic

        critical_5 = anderson_result.critical_values[2]

        ad_result = (
            "Fail to Reject Normality"
            if ad_stat < critical_5
            else "Reject Normality"
        )

        self.tree.insert(
            "",
            "end",
            values=(
                "Anderson-Darling",
                round(ad_stat, 5),
                "Critical Value Method",
                ad_result
            )
        )

        messagebox.showinfo(
            "Done",
            "All normality tests completed!"
        )


# ==========================================================
# RUN APPLICATION
# ==========================================================

root = tk.Tk()

app = StatsAnalysisApp(root)

root.mainloop()
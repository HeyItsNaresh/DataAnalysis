# ==========================================================
# STATISTICAL ANALYSIS TOOLKIT
# Tasks 2–6
# Descriptive Statistics
# PDF / CDF
# Distribution Fitting
# Q-Q Plot
# Central Limit Theorem
# ==========================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import (
    skew,
    kurtosis,
    gaussian_kde,
    norm,
    uniform,
    expon,
    kstest
)

# ==========================================================
# MAIN APPLICATION
# ==========================================================

class StatisticalAnalysisApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Statistical Analysis Toolkit")
        self.root.geometry("1050x760")

        self.df = None
        self.numeric_columns = []
        self.fitted_results = {}

        # ======================================================
        # TITLE
        # ======================================================

        title = tk.Label(
            root,
            text="Statistical Analysis Toolkit",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            root,
            text="Upload CSV • Statistics • PDF/CDF • Distribution Fitting • Q-Q Plot • CLT",
            font=("Arial", 11),
            fg="gray"
        )
        subtitle.pack()

        # ======================================================
        # UPLOAD BUTTON
        # ======================================================

        upload_btn = tk.Button(
            root,
            text="Upload CSV File",
            command=self.upload_csv,
            font=("Arial", 12),
            width=25
        )
        upload_btn.pack(pady=12)

        # ======================================================
        # FILE LABEL
        # ======================================================

        self.file_label = tk.Label(
            root,
            text="No file uploaded",
            font=("Arial", 10),
            fg="gray"
        )
        self.file_label.pack()

        # ======================================================
        # COLUMN SELECTION
        # ======================================================

        selection_frame = tk.Frame(root)
        selection_frame.pack(pady=15)

        column_label = tk.Label(
            selection_frame,
            text="Select Continuous/Numeric Column:",
            font=("Arial", 12)
        )
        column_label.grid(row=0, column=0, padx=10)

        self.column_dropdown = ttk.Combobox(
            selection_frame,
            state="readonly",
            width=35
        )
        self.column_dropdown.grid(row=0, column=1, padx=10)

        # ======================================================
        # BUTTONS
        # ======================================================

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        buttons = [
            ("Calculate Statistics", self.calculate_statistics),
            ("Generate PDF Plot", self.generate_pdf),
            ("Generate CDF Plot", self.generate_cdf),
            ("Fit Distributions", self.fit_distributions),
            ("Generate Q-Q Plot", self.generate_qq_plot),
            ("Demonstrate CLT", self.demonstrate_clt)
        ]

        for i, (text, command) in enumerate(buttons):

            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 10),
                width=22
            )

            btn.grid(
                row=i // 3,
                column=i % 3,
                padx=8,
                pady=6
            )

        # ======================================================
        # TABLE
        # ======================================================

        table_label = tk.Label(
            root,
            text="Output Table",
            font=("Arial", 14, "bold")
        )
        table_label.pack(pady=8)

        self.tree = ttk.Treeview(
            root,
            columns=("Column1", "Column2", "Column3", "Column4"),
            show="headings",
            height=18
        )

        self.tree.heading("Column1", text="Item")
        self.tree.heading("Column2", text="Value 1")
        self.tree.heading("Column3", text="Value 2")
        self.tree.heading("Column4", text="Value 3")

        self.tree.column("Column1", width=280, anchor="center")
        self.tree.column("Column2", width=230, anchor="center")
        self.tree.column("Column3", width=230, anchor="center")
        self.tree.column("Column4", width=230, anchor="center")

        self.tree.pack(
            pady=10,
            fill="both",
            expand=True
        )

        # ======================================================
        # STATUS LABEL
        # ======================================================

        self.status_label = tk.Label(
            root,
            text="Upload a CSV dataset to begin.",
            font=("Arial", 10),
            fg="blue"
        )

        self.status_label.pack(pady=8)

    # ==========================================================
    # HELPER METHODS
    # ==========================================================

    def clear_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

    def insert_row(self, c1="", c2="", c3="", c4=""):

        self.tree.insert(
            "",
            "end",
            values=(c1, c2, c3, c4)
        )

    def round_val(self, value):

        if isinstance(value, (int, float, np.number)):
            return round(value, 4)

        return value

    def get_selected_data(self):

        if self.df is None:

            messagebox.showwarning(
                "No File",
                "Please upload a CSV file first."
            )

            return None, None

        selected_column = self.column_dropdown.get()

        if not selected_column:

            messagebox.showwarning(
                "No Column",
                "Please select a numeric column."
            )

            return None, None

        data = self.df[selected_column].dropna()

        if len(data) < 2:

            messagebox.showerror(
                "Error",
                "Not enough numeric data."
            )

            return None, None

        return selected_column, np.array(data)

    # ==========================================================
    # UPLOAD CSV
    # ==========================================================

    def upload_csv(self):

        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        try:

            self.df = pd.read_csv(file_path)

            if self.df.empty:

                messagebox.showerror(
                    "Error",
                    "CSV file is empty."
                )

                return

            self.numeric_columns = self.df.select_dtypes(
                include=np.number
            ).columns.tolist()

            if not self.numeric_columns:

                messagebox.showerror(
                    "Error",
                    "No numeric columns found."
                )

                return

            self.column_dropdown["values"] = self.numeric_columns
            self.column_dropdown.current(0)

            filename = file_path.split("/")[-1]

            self.file_label.config(
                text=f"Loaded File: {filename}",
                fg="green"
            )

            self.status_label.config(
                text=f"Dataset loaded successfully. Numeric columns found: {len(self.numeric_columns)}",
                fg="green"
            )

            self.clear_table()

        except Exception as e:

            messagebox.showerror(
                "File Error",
                f"Could not load CSV.\n\nError:\n{e}"
            )

    # ==========================================================
    # TASK 2 - DESCRIPTIVE STATISTICS
    # ==========================================================

    def calculate_statistics(self):

        selected_column, data = self.get_selected_data()

        if data is None:
            return

        if len(data) < 100:

            messagebox.showwarning(
                "Warning",
                f"The selected column contains only {len(data)} observations.\n"
                "Assignment requires at least 100 observations."
            )

        mean_val = np.mean(data)
        median_val = np.median(data)

        mode_series = pd.Series(data).mode()
        mode_val = mode_series.iloc[0] if not mode_series.empty else "No mode"

        range_val = np.max(data) - np.min(data)

        variance_val = np.var(data, ddof=1)

        std_val = np.std(data, ddof=1)

        skewness_val = skew(data)

        kurtosis_val = kurtosis(data)

        min_val = np.min(data)

        max_val = np.max(data)

        q1 = np.percentile(data, 25)
        q2 = np.percentile(data, 50)
        q3 = np.percentile(data, 75)

        stats = [
            ("Mean", mean_val),
            ("Median", median_val),
            ("Mode", mode_val),
            ("Range", range_val),
            ("Variance", variance_val),
            ("Standard Deviation", std_val),
            ("Skewness", skewness_val),
            ("Kurtosis", kurtosis_val),
            ("Minimum", min_val),
            ("Maximum", max_val),
            ("Q1 (25%)", q1),
            ("Q2 (50%)", q2),
            ("Q3 (75%)", q3),
            ("Observations", len(data))
        ]

        self.clear_table()

        for stat, value in stats:

            self.insert_row(
                stat,
                self.round_val(value)
            )

        self.status_label.config(
            text=f"Statistics calculated for: {selected_column}",
            fg="green"
        )

    # ==========================================================
    # TASK 3 - PDF
    # ==========================================================

    def generate_pdf(self):

        selected_column, data = self.get_selected_data()

        if data is None:
            return

        try:

            kde = gaussian_kde(data)

            x_vals = np.linspace(
                np.min(data),
                np.max(data),
                500
            )

            y_vals = kde(x_vals)

            plt.figure(figsize=(10, 6))

            plt.hist(
                data,
                bins=30,
                density=True,
                alpha=0.6,
                edgecolor='black'
            )

            plt.plot(
                x_vals,
                y_vals,
                linewidth=2
            )

            plt.title(f"PDF Plot - {selected_column}")

            plt.xlabel(selected_column)

            plt.ylabel("Density")

            plt.grid(True)

            plt.show()

        except Exception as e:

            messagebox.showerror(
                "PDF Error",
                f"Could not generate PDF plot.\n\nError:\n{e}"
            )

    # ==========================================================
    # TASK 3 - CDF
    # ==========================================================

    def generate_cdf(self):

        selected_column, data = self.get_selected_data()

        if data is None:
            return

        try:

            sorted_data = np.sort(data)

            cdf = np.arange(
                1,
                len(sorted_data) + 1
            ) / len(sorted_data)

            plt.figure(figsize=(10, 6))

            plt.plot(
                sorted_data,
                cdf,
                linewidth=2
            )

            plt.title(f"CDF Plot - {selected_column}")

            plt.xlabel(selected_column)

            plt.ylabel("Cumulative Probability")

            plt.grid(True)

            plt.show()

        except Exception as e:

            messagebox.showerror(
                "CDF Error",
                f"Could not generate CDF plot.\n\nError:\n{e}"
            )

    # ==========================================================
    # TASK 4 - FIT DISTRIBUTIONS
    # Normal, Uniform, Exponential
    # ==========================================================

    def fit_distributions(self):

        selected_column, data = self.get_selected_data()

        if data is None:
            return

        try:

            distributions = {
                "Normal": norm,
                "Uniform": uniform,
                "Exponential": expon
            }

            self.fitted_results = {}

            x_vals = np.linspace(
                np.min(data),
                np.max(data),
                500
            )

            plt.figure(figsize=(10, 6))

            plt.hist(
                data,
                bins=30,
                density=True,
                alpha=0.5,
                edgecolor='black',
                label='Observed Data'
            )

            self.clear_table()

            self.insert_row(
                "Distribution",
                "Parameters",
                "KS Statistic",
                "p-value"
            )

            for name, dist in distributions.items():

                params = dist.fit(data)

                pdf_vals = dist.pdf(
                    x_vals,
                    *params
                )

                ks_stat, p_value = kstest(
                    data,
                    dist.cdf,
                    args=params
                )

                log_likelihood = np.sum(
                    dist.logpdf(data, *params)
                )

                k = len(params)

                aic = 2 * k - 2 * log_likelihood

                bic = k * np.log(len(data)) - 2 * log_likelihood

                self.fitted_results[name] = {
                    "distribution": dist,
                    "params": params,
                    "aic": aic
                }

                plt.plot(
                    x_vals,
                    pdf_vals,
                    linewidth=2,
                    label=name
                )

                param_text = ", ".join(
                    [str(round(p, 4)) for p in params]
                )

                self.insert_row(
                    name,
                    param_text,
                    round(ks_stat, 4),
                    round(p_value, 4)
                )

                self.insert_row(
                    f"{name} AIC/BIC",
                    round(aic, 4),
                    round(bic, 4),
                    ""
                )

            plt.title(
                f"Fitted Distribution PDFs - {selected_column}"
            )

            plt.xlabel(selected_column)

            plt.ylabel("Density")

            plt.legend()

            plt.grid(True)

            plt.show()

            best_fit = min(
                self.fitted_results,
                key=lambda d: self.fitted_results[d]["aic"]
            )

            self.status_label.config(
                text=f"Distribution fitting complete. Best fit: {best_fit}",
                fg="green"
            )

        except Exception as e:

            messagebox.showerror(
                "Fitting Error",
                f"Could not fit distributions.\n\nError:\n{e}"
            )

    # ==========================================================
    # TASK 5 - Q-Q PLOT
    # ==========================================================

    def generate_qq_plot(self):

        selected_column, data = self.get_selected_data()

        if data is None:
            return

        try:

            if not self.fitted_results:

                messagebox.showinfo(
                    "Info",
                    "No fitted distributions found.\n"
                    "The app will fit distributions first."
                )

                self.fit_distributions()

            best_fit_name = min(
                self.fitted_results,
                key=lambda d: self.fitted_results[d]["aic"]
            )

            dist = self.fitted_results[best_fit_name]["distribution"]

            params = self.fitted_results[best_fit_name]["params"]

            sorted_data = np.sort(data)

            n = len(sorted_data)

            probabilities = (
                np.arange(1, n + 1) - 0.5
            ) / n

            theoretical_quantiles = dist.ppf(
                probabilities,
                *params
            )

            plt.figure(figsize=(8, 8))

            plt.scatter(
                theoretical_quantiles,
                sorted_data,
                alpha=0.7
            )

            min_val = min(
                np.min(theoretical_quantiles),
                np.min(sorted_data)
            )

            max_val = max(
                np.max(theoretical_quantiles),
                np.max(sorted_data)
            )

            plt.plot(
                [min_val, max_val],
                [min_val, max_val],
                linestyle='--'
            )

            plt.title(
                f"Q-Q Plot: {selected_column} vs {best_fit_name}"
            )

            plt.xlabel(
                f"Theoretical Quantiles ({best_fit_name})"
            )

            plt.ylabel("Observed Quantiles")

            plt.grid(True)

            plt.show()

            self.status_label.config(
                text=f"Q-Q plot generated using {best_fit_name} distribution.",
                fg="green"
            )

        except Exception as e:

            messagebox.showerror(
                "Q-Q Plot Error",
                f"Could not generate Q-Q plot.\n\nError:\n{e}"
            )

    # ==========================================================
    # TASK 6 - CENTRAL LIMIT THEOREM
    # ==========================================================

    def demonstrate_clt(self):

        selected_column, data = self.get_selected_data()

        if data is None:
            return

        try:

            sample_size = 30

            number_of_samples = 1000

            sample_means = []

            for _ in range(number_of_samples):

                sample = np.random.choice(
                    data,
                    size=sample_size,
                    replace=True
                )

                sample_means.append(
                    np.mean(sample)
                )

            sample_means = np.array(sample_means)

            plt.figure(figsize=(10, 6))

            plt.hist(
                sample_means,
                bins=30,
                density=True,
                alpha=0.6,
                edgecolor='black'
            )

            kde = gaussian_kde(sample_means)

            x_vals = np.linspace(
                np.min(sample_means),
                np.max(sample_means),
                500
            )

            y_vals = kde(x_vals)

            plt.plot(
                x_vals,
                y_vals,
                linewidth=2
            )

            plt.title(
                "Central Limit Theorem Demonstration"
            )

            plt.xlabel(
                f"Sample Means of {selected_column}"
            )

            plt.ylabel("Density")

            plt.grid(True)

            plt.show()

            self.clear_table()

            self.insert_row(
                "CLT Metric",
                "Value"
            )

            self.insert_row(
                "Original Mean",
                self.round_val(np.mean(data))
            )

            self.insert_row(
                "Mean of Sample Means",
                self.round_val(np.mean(sample_means))
            )

            self.insert_row(
                "Original Std Dev",
                self.round_val(np.std(data))
            )

            self.insert_row(
                "Std Dev of Sample Means",
                self.round_val(np.std(sample_means))
            )

            self.insert_row(
                "Sample Size",
                sample_size
            )

            self.insert_row(
                "Number of Samples",
                number_of_samples
            )

            self.status_label.config(
                text="CLT demonstration completed.",
                fg="green"
            )

        except Exception as e:

            messagebox.showerror(
                "CLT Error",
                f"Could not demonstrate CLT.\n\nError:\n{e}"
            )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = StatisticalAnalysisApp(root)

    root.mainloop()
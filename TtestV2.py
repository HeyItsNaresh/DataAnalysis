import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats


class TTestToolkitApp:

    def __init__(self, root):

        self.root = root
        self.root.title("T-Test Statistical Toolkit")
        self.root.geometry("1300x800")

        self.df = None
        self.alpha = 0.05

        self.build_ui()

    # =========================================================
    # UI
    # =========================================================

    def build_ui(self):

        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main, width=360)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        title = ttk.Label(
            left,
            text="T-Test Statistical Toolkit",
            font=("Arial", 18, "bold")
        )
        title.pack(anchor="w", pady=(0, 10))

        ttk.Button(
            left,
            text="Upload CSV / Excel File",
            command=self.load_file
        ).pack(fill=tk.X, pady=4)

        self.file_label = ttk.Label(
            left,
            text="No file loaded",
            wraplength=320
        )
        self.file_label.pack(anchor="w", pady=(2, 10))

        ttk.Label(
            left,
            text="0. Data Description and Source",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.desc_text = tk.Text(left, height=5)
        self.desc_text.pack(fill=tk.X, pady=(4, 10))

        self.desc_text.insert(
            "1.0",
            "Dataset source: Enter source here.\n"
            "Description: Enter dataset description here."
        )

        ttk.Label(
            left,
            text="Choose t-test type",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.test_type = tk.StringVar(
            value="One-Sample t-Test"
        )

        dropdown = ttk.Combobox(
            left,
            textvariable=self.test_type,
            values=[
                "One-Sample t-Test",
                "Independent Two-Sample t-Test",
                "Paired t-Test"
            ],
            state="readonly"
        )

        dropdown.pack(fill=tk.X, pady=4)

        dropdown.bind(
            "<<ComboboxSelected>>",
            lambda e: self.update_controls()
        )

        ttk.Separator(left).pack(fill=tk.X, pady=10)

        self.controls_frame = ttk.Frame(left)
        self.controls_frame.pack(fill=tk.X)

        self.update_controls()

        ttk.Separator(left).pack(fill=tk.X, pady=10)

        ttk.Label(
            left,
            text="Alternative Hypothesis",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.alt_var = tk.StringVar(value="two-sided")

        ttk.Combobox(
            left,
            textvariable=self.alt_var,
            values=["two-sided", "greater", "less"],
            state="readonly"
        ).pack(fill=tk.X, pady=4)

        ttk.Label(
            left,
            text="Significance Level α",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(8, 0))

        self.alpha_var = tk.StringVar(value="0.05")

        ttk.Entry(
            left,
            textvariable=self.alpha_var
        ).pack(fill=tk.X, pady=4)

        ttk.Button(
            left,
            text="Run Analysis",
            command=self.run_analysis
        ).pack(fill=tk.X, pady=(12, 4))

        # =====================================================
        # NOTEBOOK
        # =====================================================

        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.results_tab = ttk.Frame(self.notebook)
        self.plot_tab = ttk.Frame(self.notebook)
        self.assumption_tab = ttk.Frame(self.notebook)
        self.conclusion_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.results_tab, text="Results")
        self.notebook.add(self.plot_tab, text="Visualization")
        self.notebook.add(self.assumption_tab, text="Assumptions")
        self.notebook.add(self.conclusion_tab, text="Conclusion")

        self.results_text = tk.Text(
            self.results_tab,
            font=("Consolas", 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        self.assumption_text = tk.Text(
            self.assumption_tab,
            font=("Consolas", 10)
        )
        self.assumption_text.pack(fill=tk.BOTH, expand=True)

        self.conclusion_text = tk.Text(
            self.conclusion_tab,
            font=("Arial", 11)
        )
        self.conclusion_text.pack(fill=tk.BOTH, expand=True)

    # =========================================================
    # FILE LOADING
    # =========================================================

    def load_file(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("CSV Files", "*.csv"),
                ("Excel Files", "*.xlsx *.xls")
            ]
        )

        if not path:
            return

        try:

            if path.endswith(".csv"):
                self.df = pd.read_csv(path)
            else:
                self.df = pd.read_excel(path)

            self.file_label.config(
                text=f"Loaded: {path.split('/')[-1]}"
            )

            self.update_controls()

            messagebox.showinfo(
                "Success",
                "Dataset loaded successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =========================================================
    # CONTROLS
    # =========================================================

    def get_numeric_columns(self):

        if self.df is None:
            return []

        return list(
            self.df.select_dtypes(include=[np.number]).columns
        )

    def update_controls(self):

        for widget in self.controls_frame.winfo_children():
            widget.destroy()

        ttk.Label(
            self.controls_frame,
            text="Column Selection",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.col1_var = tk.StringVar()
        self.col2_var = tk.StringVar()
        self.group_var = tk.StringVar()
        self.mu_var = tk.StringVar(value="0")

        numeric_columns = self.get_numeric_columns()

        all_columns = (
            list(self.df.columns)
            if self.df is not None
            else []
        )

        test = self.test_type.get()

        # =====================================================
        # INDEPENDENT TEST
        # =====================================================

        if test == "Independent Two-Sample t-Test":

            ttk.Label(
                self.controls_frame,
                text="Numeric Test Column"
            ).pack(anchor="w", pady=(6, 0))

            self.col1_combo = ttk.Combobox(
                self.controls_frame,
                textvariable=self.col1_var,
                values=numeric_columns,
                state="readonly"
            )

            self.col1_combo.pack(fill=tk.X, pady=3)

            if numeric_columns:
                self.col1_var.set(numeric_columns[0])

            ttk.Label(
                self.controls_frame,
                text="Grouping Column"
            ).pack(anchor="w", pady=(6, 0))

            self.group_combo = ttk.Combobox(
                self.controls_frame,
                textvariable=self.group_var,
                values=all_columns,
                state="readonly"
            )

            self.group_combo.pack(fill=tk.X, pady=3)

            if all_columns:
                self.group_var.set(all_columns[0])

        # =====================================================
        # ONE SAMPLE + PAIRED
        # =====================================================

        else:

            ttk.Label(
                self.controls_frame,
                text="Column 1"
            ).pack(anchor="w", pady=(6, 0))

            self.col1_combo = ttk.Combobox(
                self.controls_frame,
                textvariable=self.col1_var,
                values=numeric_columns,
                state="readonly"
            )

            self.col1_combo.pack(fill=tk.X, pady=3)

            if numeric_columns:
                self.col1_var.set(numeric_columns[0])

            if test == "Paired t-Test":

                ttk.Label(
                    self.controls_frame,
                    text="Column 2"
                ).pack(anchor="w", pady=(6, 0))

                self.col2_combo = ttk.Combobox(
                    self.controls_frame,
                    textvariable=self.col2_var,
                    values=numeric_columns,
                    state="readonly"
                )

                self.col2_combo.pack(fill=tk.X, pady=3)

                if len(numeric_columns) > 1:
                    self.col2_var.set(numeric_columns[1])

            if test == "One-Sample t-Test":

                ttk.Label(
                    self.controls_frame,
                    text="Hypothesized Mean μ₀"
                ).pack(anchor="w", pady=(6, 0))

                ttk.Entry(
                    self.controls_frame,
                    textvariable=self.mu_var
                ).pack(fill=tk.X, pady=3)

    # =========================================================
    # RUN ANALYSIS
    # =========================================================

    def run_analysis(self):

        if self.df is None:

            messagebox.showwarning(
                "No Data",
                "Please upload a dataset first."
            )

            return

        self.alpha = float(self.alpha_var.get())

        test = self.test_type.get()

        if test == "One-Sample t-Test":
            self.run_one_sample()

        elif test == "Independent Two-Sample t-Test":
            self.run_independent()

        else:
            self.run_paired()

    # =========================================================
    # ONE SAMPLE
    # =========================================================

    def run_one_sample(self):

        col = self.col1_var.get()

        data = pd.to_numeric(
            self.df[col],
            errors="coerce"
        ).dropna()

        mu0 = float(self.mu_var.get())

        result = stats.ttest_1samp(
            data,
            popmean=mu0
        )

        mean = data.mean()

        ci = stats.t.interval(
            0.95,
            len(data)-1,
            loc=mean,
            scale=stats.sem(data)
        )

        self.show_results(
            "One-Sample t-Test",
            result,
            len(data)-1,
            mean,
            ci
        )

        self.plot_one_sample(data, mu0)

    # =========================================================
    # INDEPENDENT
    # =========================================================

    def run_independent(self):

        value_col = self.col1_var.get()
        group_col = self.group_var.get()

        temp_df = self.df[
            [value_col, group_col]
        ].dropna()

        groups = temp_df[group_col].unique()

        if len(groups) != 2:

            messagebox.showerror(
                "Error",
                "Grouping column must contain exactly 2 groups."
            )

            return

        group1 = groups[0]
        group2 = groups[1]

        x = pd.to_numeric(
            temp_df[
                temp_df[group_col] == group1
            ][value_col],
            errors="coerce"
        ).dropna()

        y = pd.to_numeric(
            temp_df[
                temp_df[group_col] == group2
            ][value_col],
            errors="coerce"
        ).dropna()

        levene = stats.levene(x, y)

        equal_var = levene.pvalue >= self.alpha

        result = stats.ttest_ind(
            x,
            y,
            equal_var=equal_var
        )

        diff = x.mean() - y.mean()

        se = np.sqrt(
            x.var(ddof=1)/len(x)
            +
            y.var(ddof=1)/len(y)
        )

        df = len(x) + len(y) - 2

        critical = stats.t.ppf(
            0.975,
            df
        )

        ci = (
            diff - critical * se,
            diff + critical * se
        )

        self.show_results(
            "Independent Two-Sample t-Test",
            result,
            df,
            diff,
            ci
        )

        self.plot_independent(
            x,
            y,
            str(group1),
            str(group2)
        )

    # =========================================================
    # PAIRED
    # =========================================================

    def run_paired(self):

        col1 = self.col1_var.get()
        col2 = self.col2_var.get()

        pair_df = self.df[
            [col1, col2]
        ].dropna()

        x = pd.to_numeric(
            pair_df[col1],
            errors="coerce"
        )

        y = pd.to_numeric(
            pair_df[col2],
            errors="coerce"
        )

        result = stats.ttest_rel(x, y)

        diff = x - y

        mean_diff = diff.mean()

        ci = stats.t.interval(
            0.95,
            len(diff)-1,
            loc=mean_diff,
            scale=stats.sem(diff)
        )

        self.show_results(
            "Paired t-Test",
            result,
            len(diff)-1,
            mean_diff,
            ci
        )

        self.plot_paired(x, y)

    # =========================================================
    # RESULTS
    # =========================================================

    def show_results(
        self,
        title,
        result,
        df,
        mean,
        ci
    ):

        self.results_text.delete("1.0", tk.END)

        decision = (
            "Reject H₀"
            if result.pvalue < self.alpha
            else "Fail to Reject H₀"
        )

        # =====================================================
        # ONE-SAMPLE
        # =====================================================

        if title == "One-Sample t-Test":

            col = self.col1_var.get()

            data = pd.to_numeric(
                self.df[col],
                errors="coerce"
            ).dropna()

            sample_size = len(data)

            sample_mean = data.mean()

            mean_difference = (
                sample_mean - float(self.mu_var.get())
            )

            h0 = (
                f"H₀: The population mean of "
                f"{col} is equal to {self.mu_var.get()}."
            )

            ha = (
                f"Hₐ: The population mean of "
                f"{col} is NOT equal to {self.mu_var.get()}."
            )

            extra_info = f"""
Sample Size:
{sample_size}

Sample Mean:
{sample_mean:.4f}

Mean Difference:
{mean_difference:.4f}
"""

        # =====================================================
        # INDEPENDENT TWO-SAMPLE
        # =====================================================

        elif title == "Independent Two-Sample t-Test":

            value_col = self.col1_var.get()

            group_col = self.group_var.get()

            temp_df = self.df[
                [value_col, group_col]
            ].dropna()

            groups = temp_df[group_col].unique()

            g1 = groups[0]
            g2 = groups[1]

            x = pd.to_numeric(
                temp_df[
                    temp_df[group_col] == g1
                ][value_col],
                errors="coerce"
            ).dropna()

            y = pd.to_numeric(
                temp_df[
                    temp_df[group_col] == g2
                ][value_col],
                errors="coerce"
            ).dropna()

            h0 = (
                f"H₀: The mean of {value_col} "
                f"for {g1} is equal to the mean "
                f"for {g2}."
            )

            ha = (
                f"Hₐ: The mean of {value_col} "
                f"for {g1} is NOT equal to the mean "
                f"for {g2}."
            )

            extra_info = f"""
Group 1:
{g1}

Group 2:
{g2}

Sample Size ({g1}):
{len(x)}

Sample Size ({g2}):
{len(y)}

Sample Mean ({g1}):
{x.mean():.4f}

Sample Mean ({g2}):
{y.mean():.4f}

Mean Difference:
{x.mean() - y.mean():.4f}
"""

        # =====================================================
        # PAIRED
        # =====================================================

        else:

            col1 = self.col1_var.get()
            col2 = self.col2_var.get()

            pair_df = self.df[
                [col1, col2]
            ].dropna()

            x = pd.to_numeric(
                pair_df[col1],
                errors="coerce"
            )

            y = pd.to_numeric(
                pair_df[col2],
                errors="coerce"
            )

            differences = x - y

            h0 = (
                f"H₀: The mean difference between "
                f"{col1} and {col2} is equal to 0."
            )

            ha = (
                f"Hₐ: The mean difference between "
                f"{col1} and {col2} is NOT equal to 0."
            )

            extra_info = f"""
Number of Pairs:
{len(differences)}

Sample Mean ({col1}):
{x.mean():.4f}

Sample Mean ({col2}):
{y.mean():.4f}

Mean Difference:
{differences.mean():.4f}
"""

        # =====================================================
        # OUTPUT
        # =====================================================

        output = f"""
{title}

==================================================

NULL HYPOTHESIS (H₀)

{h0}

--------------------------------------------------

ALTERNATIVE HYPOTHESIS (Hₐ)

{ha}

==================================================

{extra_info}

--------------------------------------------------

t-statistic:
{result.statistic:.4f}

Degrees of Freedom:
{df:.4f}

p-value:
{result.pvalue:.6f}

95% Confidence Interval:
[{ci[0]:.4f}, {ci[1]:.4f}]

Significance Level α:
{self.alpha}

==================================================

DECISION

{decision}

==================================================
"""

        self.results_text.insert(
            tk.END,
            output
        )

        # =====================================================
        # ASSUMPTIONS
        # =====================================================

        self.assumption_text.delete("1.0", tk.END)

        self.assumption_text.insert(
            tk.END,
            "ASSUMPTION CHECKS\n\n"
            "1. Data should be approximately normally distributed.\n"
            "2. Observations should be independent.\n"
            "3. Independent two-sample tests also check equality of variances using Levene's test.\n"
        )

        # =====================================================
        # CONCLUSION
        # =====================================================

        self.conclusion_text.delete("1.0", tk.END)

        self.conclusion_text.insert(
            tk.END,
            f"At the significance level α = {self.alpha}, "
            f"the test produced a p-value of "
            f"{result.pvalue:.6f}. "
            f"Based on this result, we "
            f"{decision.lower()}. "
            f"This means the statistical evidence "
            f"{'supports' if result.pvalue < self.alpha else 'does not support'} "
            f"the alternative hypothesis."
        )

    # =========================================================
    # PLOTS
    # =========================================================

    def clear_plot(self):

        for widget in self.plot_tab.winfo_children():
            widget.destroy()

    def show_plot(self, fig):

        self.clear_plot()

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.plot_tab
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    def plot_one_sample(self, data, mu0):

        fig, ax = plt.subplots(figsize=(7, 5))

        ax.hist(
            data,
            bins=20,
            edgecolor="black"
        )

        ax.axvline(
            mu0,
            linestyle="--",
            linewidth=2,
            color="red"
        )

        ax.set_title("One-Sample t-Test")

        self.show_plot(fig)

    def plot_independent(self, x, y, g1, g2):

        fig, ax = plt.subplots(figsize=(7, 5))

        ax.boxplot(
            [x, y],
            labels=[g1, g2]
        )

        ax.set_title(
            "Independent Two-Sample t-Test"
        )

        self.show_plot(fig)


    def plot_paired(self, x, y):

        fig, ax = plt.subplots(figsize=(7, 5))

        # scatter points
        ax.scatter(
            x,
            y,
            color="blue"
        )

        # diagonal reference line
        min_val = min(x.min(), y.min())
        max_val = max(x.max(), y.max())

        ax.plot(
            [min_val, max_val],
            [min_val, max_val],
            linestyle="--",
            color="red",
            linewidth=2,
            label="Before = After"
        )

        ax.legend()

        ax.set_title("Paired t-Test")

        ax.set_xlabel("Before Scores")

        ax.set_ylabel("After Scores")

        self.show_plot(fig)



# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TTestToolkitApp(root)

    root.mainloop()

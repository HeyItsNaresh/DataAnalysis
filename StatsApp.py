import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = None

# -------- HELPERS --------
def is_numeric(series):
    return pd.api.types.is_numeric_dtype(series)

# -------- LOAD FILE --------
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)

        if df.shape[1] < 2:
            messagebox.showerror("Error", "File must have at least 2 columns")
            return

        df = df.iloc[:, :2]
        df.columns = ['X', 'Y']

        # Clean Y (must be numeric)
        df['Y'] = pd.to_numeric(df['Y'], errors='coerce')

        # Try numeric conversion for X but allow strings
        df['X_numeric'] = pd.to_numeric(df['X'], errors='coerce')

        # Drop rows where Y is invalid
        before = len(df)
        df = df.dropna(subset=['Y'])
        after = len(df)

        if before != after:
            messagebox.showwarning("Warning", f"{before - after} invalid rows removed from Y")

        messagebox.showinfo("Success", "File loaded successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------- STATS --------
def compute_stats(series):
    return {
        "Mean": np.mean(series),
        "Median": np.median(series),
        "Mode": series.mode()[0] if not series.mode().empty else "N/A",
        "Min": np.min(series),
        "Max": np.max(series),
        "Range": np.max(series) - np.min(series),
        "Variance": np.var(series),
        "Std Dev": np.std(series),
        "Skewness": series.skew(),
        "Kurtosis": series.kurt()
    }

def show_stats():
    if df is None:
        return

    text_output.delete(1.0, tk.END)

    # Y stats
    stats_y = compute_stats(df['Y'])

    text_output.insert(tk.END, "=== Y Statistics ===\n")
    for k, v in stats_y.items():
        text_output.insert(tk.END, f"{k}: {v:.4f}\n")

    # X stats only if numeric
    if df['X_numeric'].notna().all():
        stats_x = compute_stats(df['X_numeric'])
        text_output.insert(tk.END, "\n=== X Statistics ===\n")
        for k, v in stats_x.items():
            text_output.insert(tk.END, f"{k}: {v:.4f}\n")

        corr = df[['X_numeric', 'Y']].corr().iloc[0,1]
        text_output.insert(tk.END, f"\nPearson Correlation: {corr:.4f}")
    else:
        text_output.insert(tk.END, "\n=== X Statistics ===\nSkipped (categorical data)\n")
        text_output.insert(tk.END, "\nPearson Correlation: Not applicable")

# -------- GROUPING --------
def get_grouped_data(mode):
    if mode == "Count":
        counts = df['X'].value_counts().reset_index()
        counts.columns = ['X', 'Value']
        return counts

    elif mode == "Percentage":
        counts = df['X'].value_counts(normalize=True).reset_index()
        counts.columns = ['X', 'Value']
        counts['Value'] *= 100
        return counts

    elif mode == "Sum":
        grouped = df.groupby('X')['Y'].sum().reset_index()
        grouped.columns = ['X', 'Value']
        return grouped

# -------- PLOTTING --------
def plot_chart():
    if df is None:
        return

    grouped = group_var.get()

    if grouped:
        chart = grouped_chart.get()
        mode = value_mode.get()
        data = get_grouped_data(mode)

        x = data['X']
        y = data['Value']

        if chart == "Bar":
            plt.bar(x, y)

        elif chart == "Pie":
            plt.pie(y, labels=x, autopct='%1.1f%%')

        elif chart == "Doughnut":
            plt.pie(y, labels=x, autopct='%1.1f%%')
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)

        plt.title(f"{chart} Chart ({mode})")
        plt.xticks(rotation=45)

    else:
        chart = chart_type.get()

        x_numeric = df['X_numeric']
        y = df['Y']

        if chart == "Scatter":
            if x_numeric.isna().any():
                messagebox.showerror("Error", "Scatter requires numeric X values")
                return

            plt.scatter(x_numeric, y)

            if regression_var.get():
                m, b = np.polyfit(x_numeric, y, 1)
                plt.plot(x_numeric, m*x_numeric + b)

        elif chart == "Line":
            if x_numeric.isna().any():
                messagebox.showerror("Error", "Line chart requires numeric X values")
                return

            plt.plot(x_numeric, y)

        elif chart == "Histogram":
            plt.hist(y, bins=10)

        elif chart == "Distribution":
            sns.histplot(y, kde=True)

        plt.xlabel("X")
        plt.ylabel("Y")

    plt.tight_layout()
    plt.show()

# -------- UI TOGGLE --------
def toggle_group():
    if group_var.get():
        grouped_chart_menu.config(state="normal")
        value_menu.config(state="normal")
        chart_menu.config(state="disabled")
    else:
        grouped_chart_menu.config(state="disabled")
        value_menu.config(state="disabled")
        chart_menu.config(state="normal")

# -------- UI --------
root = tk.Tk()
root.title("Data Analysis App")
root.geometry("700x600")

tk.Button(root, text="Upload Excel File", command=load_file).pack(pady=5)
tk.Button(root, text="Compute Statistics", command=show_stats).pack(pady=5)

chart_type = tk.StringVar(value="Scatter")
chart_menu = tk.OptionMenu(root, chart_type, "Scatter", "Line", "Histogram", "Distribution")
chart_menu.pack()

group_var = tk.BooleanVar()
tk.Checkbutton(root, text="Group X values (categorical)", variable=group_var, command=toggle_group).pack()

grouped_chart = tk.StringVar(value="Bar")
grouped_chart_menu = tk.OptionMenu(root, grouped_chart, "Bar", "Pie", "Doughnut")
grouped_chart_menu.config(state="disabled")
grouped_chart_menu.pack()

value_mode = tk.StringVar(value="Count")
value_menu = tk.OptionMenu(root, value_mode, "Count", "Percentage", "Sum")
value_menu.config(state="disabled")
value_menu.pack()

regression_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show Regression Line", variable=regression_var).pack()

tk.Button(root, text="Generate Chart", command=plot_chart).pack(pady=10)

text_output = tk.Text(root, height=15)
text_output.pack()

root.mainloop()
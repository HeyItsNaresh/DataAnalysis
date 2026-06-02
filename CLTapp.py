import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
from tkinter import ttk

# Fix randomness
np.random.seed(42)

# Simulation function
def run_simulation():
    dist_choice = dist_var.get()
    n = int(sample_size_var.get())
    num_simulations = 5000

    sample_means = []

    # Choose distribution
    if dist_choice == "Exponential":
        generator = lambda size: np.random.exponential(scale=1, size=size)
    elif dist_choice == "Uniform":
        generator = lambda size: np.random.uniform(0, 1, size=size)
    else:
        return

    # Run simulation
    for _ in range(num_simulations):
        sample = generator(n)
        sample_means.append(np.mean(sample))

    sample_means = np.array(sample_means)

    mean_val = np.mean(sample_means)
    std_val = np.std(sample_means)

    # Histogram
    plt.figure()
    plt.hist(sample_means, bins=40, density=True)

    x = np.linspace(min(sample_means), max(sample_means), 200)
    normal_curve = stats.norm.pdf(x, mean_val, std_val)
    plt.plot(x, normal_curve)

    plt.title(f"{dist_choice} | Sample Size = {n}")
    plt.xlabel("Sample Mean")
    plt.ylabel("Density")
    plt.grid()
    plt.show()

    # QQ Plot
    plt.figure()
    stats.probplot(sample_means, dist="norm", plot=plt)
    plt.title(f"QQ Plot ({dist_choice}, n={n})")
    plt.grid()
    plt.show()

    # Update result label
    result_label.config(
        text=f"Mean of Means: {mean_val:.4f} | Std Dev: {std_val:.4f}"
    )


# GUI setup
root = tk.Tk()
root.title("CLT Simulation App")
root.geometry("400x300")

# Title
title_label = tk.Label(root, text="Central Limit Theorem Simulator", font=("Arial", 14))
title_label.pack(pady=10)

# Distribution dropdown
dist_var = tk.StringVar()
dist_dropdown = ttk.Combobox(root, textvariable=dist_var)
dist_dropdown['values'] = ("Exponential", "Uniform")
dist_dropdown.current(0)
dist_dropdown.pack(pady=10)

# Sample size dropdown
sample_size_var = tk.StringVar()
sample_dropdown = ttk.Combobox(root, textvariable=sample_size_var)
sample_dropdown['values'] = ("10", "30", "100")
sample_dropdown.current(0)
sample_dropdown.pack(pady=10)

# Run button
run_button = tk.Button(root, text="Run Simulation", command=run_simulation)
run_button.pack(pady=15)

# Result label
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Run app
root.mainloop()
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
import tempfile

class WordCloudApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Cloud Generator")
        self.root.geometry("1000x700")

        self.generated_wc = None
        self.preview_photo = None

        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(
            main_frame,
            text="Word Cloud Generator",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=(0, 10))

        subtitle = ttk.Label(
            main_frame,
            text="Enter words separated by commas. Big words get the highest weight.",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 15))

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill="x", pady=5)

        # Big words
        ttk.Label(input_frame, text="Big Words").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.big_text = tk.Text(input_frame, height=5, width=50, wrap="word")
        self.big_text.grid(row=1, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")

        # Medium words
        ttk.Label(input_frame, text="Medium Words").grid(row=0, column=1, sticky="w", pady=(0, 5))
        self.medium_text = tk.Text(input_frame, height=5, width=50, wrap="word")
        self.medium_text.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky="nsew")

        # Small words
        ttk.Label(input_frame, text="Small Words").grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.small_text = tk.Text(input_frame, height=5, width=50, wrap="word")
        self.small_text.grid(row=3, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")

        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding=10)
        settings_frame.pack(fill="x", pady=10)

        ttk.Label(settings_frame, text="Width").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.width_var = tk.StringVar(value="1200")
        ttk.Entry(settings_frame, textvariable=self.width_var, width=12).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Height").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.height_var = tk.StringVar(value="700")
        ttk.Entry(settings_frame, textvariable=self.height_var, width=12).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="Background").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.bg_var = tk.StringVar(value="white")
        ttk.Entry(settings_frame, textvariable=self.bg_var, width=15).grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(settings_frame, text="Big Weight").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.big_weight_var = tk.StringVar(value="10")
        ttk.Entry(settings_frame, textvariable=self.big_weight_var, width=12).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Medium Weight").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.medium_weight_var = tk.StringVar(value="5")
        ttk.Entry(settings_frame, textvariable=self.medium_weight_var, width=12).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="Small Weight").grid(row=1, column=4, sticky="w", padx=5, pady=5)
        self.small_weight_var = tk.StringVar(value="2")
        ttk.Entry(settings_frame, textvariable=self.small_weight_var, width=12).grid(row=1, column=5, padx=5, pady=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="Generate Word Cloud", command=self.generate_wordcloud).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Preview Full Size", command=self.preview_full).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save PNG", command=self.save_png).pack(side="left", padx=5)

        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding=10)
        preview_frame.pack(fill="both", expand=True, pady=10)

        self.preview_label = ttk.Label(preview_frame, text="Your word cloud preview will appear here.")
        self.preview_label.pack(expand=True)

        sample_big = "Correlation, Relationship, Variables, Linear, Strength, Direction"
        sample_medium = "Positive, Negative, Data, Trend, Pattern, Scatter Plot, Analysis"
        sample_small = "Covariance, Deviation, Formula, Quantitative, Association"

        self.big_text.insert("1.0", sample_big)
        self.medium_text.insert("1.0", sample_medium)
        self.small_text.insert("1.0", sample_small)

    def parse_words(self, raw_text):
        return [word.strip() for word in raw_text.split(",") if word.strip()]

    def build_weighted_text(self, big_words, medium_words, small_words, big_weight, medium_weight, small_weight):
        parts = []
        parts.extend(big_words * big_weight)
        parts.extend(medium_words * medium_weight)
        parts.extend(small_words * small_weight)
        return " ".join(parts)

    def generate_wordcloud(self):
        try:
            big_words = self.parse_words(self.big_text.get("1.0", "end").strip())
            medium_words = self.parse_words(self.medium_text.get("1.0", "end").strip())
            small_words = self.parse_words(self.small_text.get("1.0", "end").strip())

            if not (big_words or medium_words or small_words):
                messagebox.showerror("Error", "Please enter at least one word.")
                return

            width = int(self.width_var.get())
            height = int(self.height_var.get())
            background = self.bg_var.get().strip() or "white"

            big_weight = int(self.big_weight_var.get())
            medium_weight = int(self.medium_weight_var.get())
            small_weight = int(self.small_weight_var.get())

            weighted_text = self.build_weighted_text(
                big_words, medium_words, small_words,
                big_weight, medium_weight, small_weight
            )

            self.generated_wc = WordCloud(
                width=width,
                height=height,
                background_color=background,
		collocations=False,
		prefer_horizontal=0.6,
		random_state=None
            ).generate(weighted_text)

            preview_path = os.path.join(tempfile.gettempdir(), "temp_preview.png")
            self.generated_wc.to_file(preview_path)

            image = Image.open(preview_path)
            image.thumbnail((850, 450))
            self.preview_photo = ImageTk.PhotoImage(image)

            self.preview_label.configure(image=self.preview_photo, text="")

        except ValueError:
            messagebox.showerror("Error", "Width, height, and weights must be numbers.")
        except Exception as exc:
            messagebox.showerror("Error", f"Something went wrong:\n{exc}")

    def preview_full(self):
        if self.generated_wc is None:
            messagebox.showinfo("Info", "Generate a word cloud first.")
            return

        plt.figure(figsize=(14, 8))
        plt.imshow(self.generated_wc, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud Preview")
        plt.show()

    def save_png(self):
        if self.generated_wc is None:
            messagebox.showinfo("Info", "Generate a word cloud first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Word Cloud"
        )

        if file_path:
            self.generated_wc.to_file(file_path)
            messagebox.showinfo("Saved", f"Word cloud saved to:\n{file_path}")


def main():
    root = tk.Tk()
    app = WordCloudApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
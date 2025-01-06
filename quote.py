import tkinter as tk
from tkinter import messagebox
import random

class QuoteGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Random Quote Generator")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        # List of quotes with their authors
        self.quotes = [
            ("Be yourself; everyone else is already taken.", "Oscar Wilde"),
            ("Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.", "Albert Einstein"),
            ("Be the change that you wish to see in the world.", "Mahatma Gandhi"),
            ("If you tell the truth, you don't have to remember anything.", "Mark Twain"),
            ("Live as if you were to die tomorrow. Learn as if you were to live forever.", "Mahatma Gandhi"),
            ("Without music, life would be a mistake.", "Friedrich Nietzsche"),
            ("To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "Ralph Waldo Emerson"),
            ("It is better to be hated for what you are than to be loved for what you are not.", "Andre Gide"),
            ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ("Life is what happens to us while we are making other plans.", "Allen Saunders")
        ]

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Random Quote Generator", 
                             font=("Helvetica", 24, "bold"), bg='#f0f0f0')
        title_label.pack(pady=20)

        # Quote Display Frame
        self.quote_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20,
                                  relief=tk.RAISED, borderwidth=2)
        self.quote_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Quote Text
        self.quote_text = tk.Label(self.quote_frame, text="Click the button to generate a quote",
                                 wraplength=500, font=("Georgia", 12), bg='#ffffff')
        self.quote_text.pack(pady=10)

        # Author Text
        self.author_text = tk.Label(self.quote_frame, text="", 
                                  font=("Georgia", 10, "italic"), bg='#ffffff')
        self.author_text.pack(pady=5)

        # Generate Button
        generate_button = tk.Button(self.root, text="Generate Quote",
                                  command=self.generate_quote,
                                  font=("Helvetica", 12),
                                  bg='#4CAF50', fg='white',
                                  padx=20, pady=10)
        generate_button.pack(pady=20)

    def generate_quote(self):
        quote, author = random.choice(self.quotes)
        self.quote_text.config(text=f'"{quote}"')
        self.author_text.config(text=f"- {author}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = QuoteGenerator()
    app.run()


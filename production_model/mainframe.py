import tkinter as tk
from PIL import ImageTk
import prod


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Продукционная модель")
        self.question_var = tk.StringVar()
        self.question = tk.Label(root, textvariable=self.question_var)
        self.question.grid(row=0, column=0, rowspan=1, columnspan=2)

        self.question_var.set("\n\nЗагадайте преподавателя\n\n")

        self.yes_button = tk.Button(root, text="Да", command=self.yes, width=30)
        self.yes_button.grid(row=1, column=0)
        self.no_button = tk.Button(root, text="Нет", command=self.no, width=30)
        self.no_button.grid(row=1, column=1)

    def yes(self):
        pass

    def no(self):
        pass

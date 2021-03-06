import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO
import requests
import prod


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Продукционная модель")

        self.model = prod.ProductionModel(self)

        self.question_var = tk.StringVar()
        self.question = tk.Label(root, textvariable=self.question_var, height=10)
        self.question.grid(row=0, column=0, rowspan=1, columnspan=2)
        self.question_var.set("\n\nЗагадайте преподавателя\n\n")

        self.lets_play_button = tk.Button(root, text="Дальше", command=self.play, width=60)
        self.lets_play_button.grid(row=1, column=0)

        self.yes_button = tk.Button(root, text="Да", command=self.yes, width=30)
        self.no_button = tk.Button(root, text="Нет", command=self.no, width=30)

        self.answer = tk.Label(root)

        self.play_more_button = tk.Button(root, command=self.play_more, text='Играть ещё', width=60)

    def play_more(self):
        self.answer.grid_forget()
        self.play_more_button.grid_forget()
        self.question_var.set("\n\nЗагадайте преподавателя\n\n")
        self.lets_play_button.grid(row=1, column=0)
        self.model.clear()

    def play(self):
        self.lets_play_button.grid_forget()
        self.answer.grid_forget()
        self.play_more_button.grid_forget()
        self.yes_button.grid(row=1, column=0)
        self.no_button.grid(row=1, column=1)
        self.model.next_step()

    def ask_question(self, question):
        self.question_var.set(question)

    def yes(self):
        self.model.set_answer('Yes')
        self.model.next_step()

    def no(self):
        self.model.set_answer('No')
        self.model.next_step()

    def put_answer(self, id):
        im = Image.open('data/' + id)
        self.pim = ImageTk.PhotoImage(im)
        self.answer.configure(image=self.pim)

        self.yes_button.grid_forget()
        self.no_button.grid_forget()
        self.answer.grid(row=1, column=0)
        self.play_more_button.grid(row=2, column=0)
        self.question_var.set('\n\nВы загадали\n\n' + self.model.teachers_names[id])


    def set_prod(self, model):
        self.model = model

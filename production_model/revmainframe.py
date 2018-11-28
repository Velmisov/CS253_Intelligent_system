import tkinter as tk
from rev_prod import ReverseProductionModel


class RevMain(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.m = ReverseProductionModel()
        self.facts = set()
        self.fact_vars = {}
        tk.Label(root, text='Факты:').grid(row=0, column=0, columnspan=2)
        i = 0
        for f in self.m.facts:
            self.fact_vars[f] = tk.IntVar()
            tk.Checkbutton(root, variable=self.fact_vars[f], onvalue=1).grid(row=1 + i, column=0)
            tk.Label(root, text=self.m.facts[f]).grid(row=1 + i, column=1)
            self.fact_vars[f].trace('w', self.fact_checked)
            i += 1
        self.teacher = ''
        self.teacher_var = tk.StringVar()
        tk.Label(root, text='Вывод:').grid(row=0, column=2, columnspan=2)
        j = 0
        for t in self.m.teachers:
            tk.Radiobutton(root, variable=self.teacher_var, value=t).grid(row=1 + j, column=2)
            tk.Label(root, text=self.m.teachers[t]).grid(row=1 + j, column=3)
            j += 1
        self.teacher_var.trace('w', self.teacher_checked)
        self.teacher_var.set('t1')

        tk.Button(root, text='Вывести', command=self.produce).grid(row=2 + max(i, j), column=0)
        self.res_label = tk.Label(root)
        self.res_label.grid(row=2 + max(i, j), column=2)

    def fact_checked(self, *args):
        self.facts = set()
        for fv in self.fact_vars:
            if self.fact_vars[fv].get() == 1:
                self.facts.add(fv)
        # print(self.facts)

    def teacher_checked(self, *args):
        self.teacher = self.teacher_var.get()
        # print(self.teacher)

    def produce(self, *args):
        self.res_label.config(text='думаю')
        res = self.m.try_produce_dfs(self.teacher, self.facts)
        self.res_label.config(text=str(res))


if __name__ == '__main__':
    root = tk.Tk()
    fr = RevMain(root)
    tk.mainloop()

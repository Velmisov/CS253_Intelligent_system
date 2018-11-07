import tkinter as tk
from mainframe import Main
from prod import ProductionModel


def main():
    root = tk.Tk()
    main = Main(root)
    tk.mainloop()


if __name__ == '__main__':
    main()

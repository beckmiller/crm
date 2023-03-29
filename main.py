import tkinter as tk
from tkinter import ttk

from tab_one import TabOne
from tab_two import TabTwo
from tab_three import TabThree
from tab_four import TabFour


class MiniCRM(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mini CRM")
        self.geometry("800x600")

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        tab_one = TabOne(notebook)
        notebook.add(tab_one, text="Прием товара")

        tab_two = TabTwo(notebook)
        notebook.add(tab_two, text="Продажа товара")

        tab_three = TabThree(notebook)
        notebook.add(tab_three, text="Возврат товара")

        tab_four = TabFour(notebook)
        notebook.add(tab_four, text="Учет и финансы")


if __name__ == "__main__":
    app = MiniCRM()
    app.mainloop()

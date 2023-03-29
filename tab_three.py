import tkinter as tk
from tkinter import ttk

class TabThree(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label = ttk.Label(self, text="Вкладка 3")
        label.pack(padx=10, pady=10)

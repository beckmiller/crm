import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime


class TabOne(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        self.treeview = ttk.Treeview(self, columns=(
            "product_name", "quantity", "purchase_date", "purchase_price", "selling_price"))
        self.treeview.heading("#0", text="ID")
        self.treeview.heading("product_name", text="Название товара")
        self.treeview.heading("quantity", text="Количество")
        self.treeview.heading("purchase_date", text="Дата закупки")
        self.treeview.heading("purchase_price", text="Цена закупки")
        self.treeview.heading("selling_price", text="Цена продажи")

        # Чтение данных из таблицы Product_batches
        cur.execute('''SELECT pb.id, p.name, pb.quantity, pb.purchase_date, pb.purchase_price, pb.selling_price 
                       FROM Product_batches AS pb JOIN Products AS p ON pb.product_id=p.id''')
        data = cur.fetchall()
        for row in data:
            self.treeview.insert("", "end", text=row[0], values=row[1:])

        self.treeview.pack(padx=10, pady=10)

        # Добавление кнопки добавления новых товаров
        add_product_button = ttk.Button(
            self, text="Добавить товар", command=self.add_product)
        add_product_button.pack(pady=10)

    def add_product(self):
        # Открытие окна для добавления нового товара
        add_product_window = AddProductWindow(self)

        if add_product_window.result is not None:
            # Добавление информации о новом товаре в базу данных
            conn = sqlite3.connect('store.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO Products (name, purchase_price, selling_price, quantity) VALUES (?, ?, ?, ?)",
                        (add_product_window.result[0], add_product_window.result[1], add_product_window.result[2], add_product_window.result[3]))
            product_id = cur.lastrowid
            cur.execute("INSERT INTO Product_batches (product_id, purchase_price, selling_price, quantity, purchase_date) VALUES (?, ?, ?, ?, ?)",
                        (product_id, add_product_window.result[1], add_product_window.result[2], add_product_window.result[3], add_product_window.result[4]))
            conn.commit()

            # Добавление информации о новом товаре в Treeview
            self.treeview.insert("", "end", text=product_id,
                                 values=add_product_window.result[:5])


class AddProductWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Добавить товар")
        self.result = None

        # Создание и расположение элементов управления
        name_label = ttk.Label(self, text="Название товара:")
        self.name_entry = ttk.Entry(self)
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        buy_price_label = ttk.Label(self, text="Цена закупки:")
        self.buy_price_entry = ttk.Entry(self)
        buy_price_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.buy_price_entry.grid(row=1, column=1, padx=5, pady=5)

        sell_price_label = ttk.Label(self, text="Цена продажи:")
        self.sell_price_entry = ttk.Entry(self)
        sell_price_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.sell_price_entry.grid(row=2, column=1, padx=5, pady=5)
        quantity_label = ttk.Label(self, text="Количество:")
        self.quantity_entry = ttk.Entry(self)
        quantity_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        purchase_date_label = ttk.Label(
            self, text="Дата закупки (ГГГГ-ММ-ДД):")
        self.purchase_date_entry = ttk.Entry(self)
        purchase_date_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.purchase_date_entry.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(self, text="Добавить",
                                command=self.add_product)
        add_button.grid(row=5, column=1, padx=5, pady=5, sticky="e")

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+{}+{}".format(parent.winfo_rootx() +
                      50, parent.winfo_rooty()+50))
        self.wait_window()

    def add_product(self):
        name = self.name_entry.get()
        buy_price = float(self.buy_price_entry.get())
        sell_price = float(self.sell_price_entry.get())
        quantity = float(self.quantity_entry.get())
        purchase_date = datetime.datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Products (name, purchase_price, selling_price, quantity) VALUES (?, ?, ?, ?)",
                    (name, buy_price, sell_price, quantity))
        product_id = cur.lastrowid
        cur.execute("INSERT INTO Product_batches (product_id, purchase_price, selling_price, quantity, purchase_date) VALUES (?, ?, ?, ?, ?)",
                    (product_id, buy_price, sell_price, quantity, purchase_date))
        conn.commit()
        self.result = "added"
        self.destroy()

    def cancel(self):
        self.destroy()

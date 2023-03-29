import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class TabTwo(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        # Создание элементов управления
        self.treeview = ttk.Treeview(
            self, columns=("product", "quantity", "date", "sale_price"))
        self.treeview.heading("#0", text="ID")
        self.treeview.heading("product", text="Название товара")
        self.treeview.heading("quantity", text="Количество")
        self.treeview.heading("date", text="Дата продажи")
        self.treeview.heading("sale_price", text="Сумма продажи")

        cur.execute('''SELECT p.id, p.name, s.quantity, s.sale_date, s.sale_price 
                       FROM Sales AS s JOIN Products AS p ON s.batch_id=p.id''')
        data = cur.fetchall()
        for row in data:
            self.treeview.insert("", "end", text=row[0], values=row[1:])

        self.treeview.pack(padx=10, pady=10)

        self.product_var = tk.StringVar()
        product_label = ttk.Label(self, text="Выберите товар:")
        product_combobox = ttk.Combobox(self, textvariable=self.product_var)
        product_label.pack(padx=10, pady=5, anchor="w")
        product_combobox.pack(padx=10, pady=5, fill="x")

        self.quantity_var = tk.DoubleVar()
        quantity_label = ttk.Label(self, text="Введите количество:")
        quantity_entry = ttk.Entry(self, textvariable=self.quantity_var)
        quantity_label.pack(padx=10, pady=5, anchor="w")
        quantity_entry.pack(padx=10, pady=5, fill="x")

        sell_button = ttk.Button(self, text="Продать",
                                 command=self.sell_product)
        sell_button.pack(padx=10, pady=10)

        # Заполнение комбобокса товарами
        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        cur.execute("SELECT name FROM Products")
        products = [product[0] for product in cur.fetchall()]
        product_combobox.config(values=products)

        # Создание фрейма для инвентаря
        self.inventory_frame = ttk.Frame(self)
        self.inventory_frame.pack(padx=10, pady=10)

    def sell_product(self):
        # Получение выбранного товара и количества
        product_name = self.product_var.get()
        quantity = self.quantity_var.get()

        # Поиск id товара в базе данных
        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        cur.execute(
            "SELECT id, selling_price FROM Products WHERE name=?", (product_name,))
        product = cur.fetchone()

        if product:
            product_id, selling_price = product

            # Поиск партий товара с достаточным количеством для продажи
            cur.execute(
                "SELECT id, quantity, purchase_price FROM Product_batches WHERE product_id=? AND quantity>=? ORDER BY purchase_date ASC", (product_id, quantity))
            batches = cur.fetchall()

            if batches:
                # Отображение окна выбора партии товара
                batch_window = tk.Toplevel(self)
                batch_window.title("Выбор партии товара")

                # Создание элементов управления для выбора партии товара
                batch_label = ttk.Label(
                    batch_window, text="Выберите партию товара:")
                batch_label.pack(padx=10, pady=5, anchor="w")

                batch_var = tk.StringVar()
                batch_radios = []
                for batch_id, batch_quantity, batch_price in batches:
                    batch_radios.append(ttk.Radiobutton(
                        batch_window, text=f"Партия {batch_id} ({batch_quantity} шт. по {batch_price} руб.)", variable=batch_var, value=batch_id))
                    batch_radios[-1].pack(padx=10, pady=2, fill="x")

                sell_button = ttk.Button(batch_window, text="Продать", command=lambda: self.sell_batch(
                    batch_var.get(), quantity, selling_price))
                sell_button.pack(padx=10, pady=10)

            else:
                # Если не найдено ни одной партии с достаточным количеством, выводим сообщение об ошибке
                tk.messagebox.showerror(
                    "Ошибка", f"Для товара '{product_name}' нет доступных партий с количеством {quantity} и более.")

    def show_inventory(self):
        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        cur.execute("SELECT Products.name, SUM(Product_batches.quantity) FROM Products LEFT JOIN Product_batches ON Products.id = Product_batches.product_id GROUP BY Products.name")
        rows = cur.fetchall()
        self.inventory_treeview = ttk.Treeview(
            self.inventory_frame, columns=(1, 2, 3, 4), show="headings", height=15)

        self.inventory_treeview.delete(*self.inventory_treeview.get_children())
        for row in rows:
            self.inventory_treeview.insert(
                "", "end", text=row[0], values=row[1])

    def sell_batch(self, batch_id, quantity, selling_price):
        # Обновление количества товара в выбранной партии и в таблице "Товары"
        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        cur.execute(
            "UPDATE Product_batches SET quantity=quantity-? WHERE id=?", (quantity, batch_id))
        cur.execute(
            "UPDATE Products SET quantity=quantity-? WHERE id=(SELECT product_id FROM Product_batches WHERE id=?)", (quantity, batch_id))

        # Вычисление цены продажи
        sale_price = selling_price * quantity

        # Добавление записи о продаже в таблицу "Продажи"
        cur.execute("INSERT INTO Sales (batch_id, quantity, sale_price, sale_date) VALUES (?, ?, ?, ?)",
                    (batch_id, quantity, sale_price, datetime.now()))

        # Сохранение изменений в базе данных
        conn.commit()

        # Обновление отображения остатков товаров и выручки
        self.show_inventory()

        # Закрытие окна выбора партии товара
        self.master.destroy()

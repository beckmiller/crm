import tkinter as tk
from tkinter import ttk

# создаем главное окно приложения
root = tk.Tk()
root.title("Мини-CRM")

# создаем вкладки
tab_control = ttk.Notebook(root)

# вкладка "Прием товара"
receive_tab = ttk.Frame(tab_control)
tab_control.add(receive_tab, text='Прием товара')

# создаем таблицу товаров
products_tree = ttk.Treeview(receive_tab, columns=('ID', 'Название товара', 'Цена закупки', 'Цена продажи', 'Количество'))
products_tree.heading('#0', text='', anchor=tk.CENTER)
products_tree.column('#0', width=0, stretch=tk.NO)
products_tree.heading('ID', text='ID', anchor=tk.CENTER)
products_tree.column('ID', width=50, anchor=tk.CENTER)
products_tree.heading('Название товара', text='Название товара', anchor=tk.CENTER)
products_tree.column('Название товара', width=200, anchor=tk.CENTER)
products_tree.heading('Цена закупки', text='Цена закупки', anchor=tk.CENTER)
products_tree.column('Цена закупки', width=150, anchor=tk.CENTER)
products_tree.heading('Цена продажи', text='Цена продажи', anchor=tk.CENTER)
products_tree.column('Цена продажи', width=150, anchor=tk.CENTER)
products_tree.heading('Количество', text='Количество', anchor=tk.CENTER)
products_tree.column('Количество', width=150, anchor=tk.CENTER)
products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# добавляем кнопки для добавления и удаления товаров
add_button = ttk.Button(receive_tab, text='Добавить товар')
add_button.pack(pady=5)

delete_button = ttk.Button(receive_tab, text='Удалить товар')
delete_button.pack()

# запускаем главный цикл обработки событий
root.mainloop()

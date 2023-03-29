import sqlite3

def create_tables():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()

    # Создание таблицы "Товары"
    c.execute('''CREATE TABLE IF NOT EXISTS Products
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                purchase_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                quantity REAL NOT NULL);''')

    # Создание таблицы "Партии товаров"
    c.execute('''CREATE TABLE IF NOT EXISTS Product_batches
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                purchase_date DATE NOT NULL,
                purchase_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                FOREIGN KEY(product_id) REFERENCES Products(id));''')

    # Создание таблицы "Продажи"
    c.execute('''CREATE TABLE IF NOT EXISTS Sales
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                sale_date DATE NOT NULL,
                FOREIGN KEY(batch_id) REFERENCES Product_batches(id));''')

    # Создание таблицы "Возвраты"
    c.execute('''CREATE TABLE IF NOT EXISTS Returns
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                return_date DATE NOT NULL,
                FOREIGN KEY(sale_id) REFERENCES Sales(id));''')

    # Создание таблицы "Финансы"
    c.execute('''CREATE TABLE IF NOT EXISTS Finances
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                revenue REAL NOT NULL,
                expenses REAL NOT NULL,
                profit REAL NOT NULL);''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print("Tables created successfully")

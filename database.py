import sqlite3
from config import DB_NAME


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total INTEGER,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_name TEXT,
        qty INTEGER,
        price INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ------------------ محصولات ------------------

def add_product(name, category, price):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO products(name, category, price) VALUES (?, ?, ?)",
        (name, category, price)
    )

    conn.commit()
    conn.close()


def get_products():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, category, price
        FROM products
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return rows


def delete_product(product_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM products WHERE id=?",
        (product_id,)
    )

    conn.commit()
    conn.close()
    # ------------------ سفارش ها ------------------

def create_order(total):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders(total) VALUES(?)",
        (total,)
    )

    order_id = cur.lastrowid

    conn.commit()
    conn.close()

    return order_id


def add_order_item(order_id, product_name, qty, price):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO order_items
        (order_id, product_name, qty, price)
        VALUES (?, ?, ?, ?)
    """, (
        order_id,
        product_name,
        qty,
        price
    ))

    conn.commit()
    conn.close()


def get_all_products():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT id,name,category,price
        FROM products
        ORDER BY category,name
    """)

    rows = cur.fetchall()

    conn.close()

    return rows
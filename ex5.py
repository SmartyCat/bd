import sqlite3 as sq

p=[
    ("Телевизор", "Электроника",20000),
    ("Микроволновка", "Электроника",8000),
    ("Книга","Книги",500),
    ("Смартфон","Электроника",15000),
    ("Ноутбук","Электроника", 45000),
    ("Журнал","Книги",300),
    ("Камера","Электроника",25000),
    ("Ручка","Канцелярия",50),
    ("Планшет","Электроника",25000),
    ("Наушники","Электроника",7000)
]

s=[
    (1,5,"2025-01-01"),
    (2,8,"2025-01-02"),
    (3,15,"2025-01-03"),
    (4,10,"2025-01-04"),
    (5,3,"2025-01-05"),
    (6,20,"2025-01-06"),
    (7,2,"2025-01-07"),
    (8,100,"2025-01-08"),
    (9,7,"2025-01-9"),
    (10,12,"2025-01-10")
]


with sq.connect('shop.db') as con:
    cur=con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        sale_date TEXT);''')

    cur.executemany("INSERT INTO products VALUES(Null,?,?,?)",p)
    cur.executemany("INSERT INTO sales VALUES(Null,?,?,?);",s)

    cur.execute("SELECT name FROM products JOIN sales ON product_id=products.id GROUP BY name HAVING price*quantity>50000")
    print(cur.fetchall())

    cur.execute("SELECT name FROM products ORDER BY price")
    print(cur.fetchall())
    cur.execute("SELECT name FROM products ORDER BY price")
    print(cur.fetchmany(5))

    cur.execute("SELECT name FROM products JOIN sales ON product_id=products.id GROUP BY name HAVING price*quantity IN (SELECT MAX(price*quantity) FROM products JOIN sales ON product_id=products.id)")
    print(cur.fetchall())

    
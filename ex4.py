import sqlite3 as sq

p=[
    ("Телевизор","Электроника",20000),
    ("Микроволновка","Электроника",8000),
    ("Книга","Книги",500),
    ("Смартфон","Электроника",15000),
    ("Ноутбук","Электроника",45000),
    ("Журнал","Книги",300)
]

s=[
    (1,5,"20205-01-01"),
    (2,8,"2025-01-02"),
    (3,15,"2025-01-03"),
    (4,10,"2025-01-04"),
    (5,3,"2025-01-05"),
    (6,20,"2025-01-06")
]

with sq.connect("test.db") as con:
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
    cur.executemany("INSERT INTO sales VALUES(Null,?,?,?)", s)

    cur.execute("SELECT category FROM products JOIN sales ON product_id=products.id GROUP BY category HAVING SUM(price*quantity)=(SELECT MAX(total) FROM (SELECT SUM(price*quantity) AS total FROM sales JOIN products ON product_id=products.id GROUP BY category))")
    print(cur.fetchall())

    cur.execute("SELECT name FROM products JOIN sales ON product_id=products.id WHERE quantity>9")
    print(cur.fetchall())

    cur.execute("SELECT name FROM products JOIN sales ON product_id=products.id GROUP BY name HAVING price*quantity>50000")
    print(cur.fetchall())

    cur.execute("SELECT name,category FROM products ORDER BY price")
    print(cur.fetchall())

    cur.execute('SELECT SUM(quantity), SUM(price) FROM products JOIN sales ON product_id=products.id GROUP BY category')
    print(cur.fetchall())

    cur.execute("SELECT name FROM products JOIN sales ON product_id=products.id WHERE quantity IN (SELECT MAX(quantity) FROM sales)")
    print(cur.fetchall())

    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("DROP TABLE IF EXISTS sales")
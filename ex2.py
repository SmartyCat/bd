import sqlite3 as sq

s=[
    ("Телевизор", "Электроника",5,2000),
    ("Миковолновка","Электроника",8,8000),
    ("Книга","Книги",15,500),
    ("Смартфон","Электроника",10,15000),
    ("Ноутбук","Электроника",3,45000),
    ("Журнал","Книги",20,300)
 ]

with sq.connect("test.db") as con:
    cur=con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS sales(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                category TEXT,
                quantity INTEGER,
                price REAL);''')
    
    cur.executemany("INSERT INTO sales VALUES(Null,?,?,?,?)", s)

    cur.execute("SELECT category FROM sales GROUP BY category HAVING SUM(price*quantity)= (SELECT MAX(total) FROM(SELECT SUM(price*quantity) AS total FROM sales GROUP BY category))")
    print(cur.fetchall())
    cur.execute("SELECT category,SUM(quantity) AS total FROM sales GROUP BY category")
    print(cur.fetchall())
    
    cur.execute("SELECT product FROM sales GROUP BY product HAVING price IN (SELECT MIN(price) FROM sales) AND quantity>0")
    print(cur.fetchall())

    cur.execute("UPDATE sales SET price=price+price*10/100 WHERE category='Книги'")

    cur.execute("DELETE FROM sales WHERE quantity<5")

    cur.execute("SELECT * FROM sales")
    print(cur.fetchall())
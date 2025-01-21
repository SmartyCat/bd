import sqlite3 as sq

b=[
    ("Мастер и Маргарита","Булгаков",55.00,33),
    ("Идиот","Дотоевский", 604.12,3),
    ("Десят Негритят","Агата Кристи",100,255),
    ("Волхв","Фаулз",123,17),
    ("Герой нашего времени","Лермонтов",505,43)
]

with sq.connect("test.db") as con:
    cur=con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            price REAL,
            quantity INTEGER
                );''')
    
    cur.executemany('''INSERT INTO books VALUES(Null,?,?,?,?);''', b)

    cur.execute('''SELECT title FROM books WHERE price>500''')
    result=cur.fetchall()
    print(result)
    cur.execute('''SELECT title FROM books WHERE author="Лермонтов"''')
    result=cur.fetchall()
    print(result)
    cur.execute('''SELECT title FROM books WHERE quantity<5''')
    print(cur.fetchall())
    cur.execute('''UPDATE books SET price=price+(price*10/100)''')
    
    cur.execute('''DELETE FROM books WHERE quantity IN (SELECT MIN(quantity) FROM books)''')

    cur.execute('''SELECT SUM(quantity) AS total_books FROM books''')

    print(cur.fetchall())

    cur.execute('''SELECT AVG(price) FROM books''')

    print(cur.fetchall())
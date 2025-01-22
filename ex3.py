import sqlite3 as sq


s=[
    ("Alice",20,"A"),
    ("Bob",21,"B"),
    ("Charlie",22,"A"),
    ("Diana",20,"C"),
    ("Eve",21,"B")
]
g=[
    (1,"Math",85,"2025-01-10"),
    (1,"History",90,"2025-01-12"),
    (2,"Math",78,"2025-01-10"),
    (3,"History",95,"2025-01-15"),
    (4,"Math",88,"2025-01-15"),
    (5,"History",72,"2025-01-16")
]

with sq.connect("test.db") as con:
    cur=con.cursor()

    cur.execute("""CREATE TABLE If NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                group_name TEXT);""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT,
                grade INTEGER,
                date TEXT);""")

    cur.executemany("INSERT INTO students VALUES(Null,?,?,?)",s)
    cur.executemany("INSERT INTO grades VALUES(Null,?,?,?,?)", g)

    cur.execute("SELECT name,group_name,subject, AVG(grade) AS aver, date FROM students JOIN grades ON students.id=student_id GROUP BY subject,name ORDER BY aver DESC")

    print(cur.fetchall())


    
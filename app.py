from flask import Flask, g,redirect,render_template, request,flash
import sqlite3 as sq

DATABASE="users.db"
SECRET_KEY="1234qwer"

app=Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    conn=sq.connect(app.config["DATABASE"])
    return conn

def create_db():
    db=connect_db()
    with app.open_resource("my_sql.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g,"link_db"):
        g.link_db=connect_db()
    return g.link_db

@app.teardown_appcontext
def close(error):
    if hasattr(g,"link_db"):
        g.link_db.close()


@app.route("/add",methods=["POST","GET"])
def main():
    db=get_db()
    if request.method=="POST":
        name=request.form.get("name")
        age=request.form.get("age")
        if name and age:
            db.cursor().execute("INSERT INTO users VALUES(Null,?,?)", (name,age))
            db.commit()
            flash("Данные успешно отправлены")
        else:
            flash("Ошибка")
    return render_template("add.html")

@app.route("/")
def add():
    db=get_db()
    users=db.cursor().execute("SELECT name, age FROM users")
    users=users.fetchall()
    return render_template("main.html",users=users)
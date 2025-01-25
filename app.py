from flask import Flask,g,render_template,flash,request
import sqlite3 as sq

DATABASE="movies.db"
DEBUG=True
SECRET_KEY="1234QWER"

app=Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    conn=sq.connect("movies.db")
    return conn

def create_db():
    db=connect_db()
    with app.open_resource("my_sql.sql",mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g,"link_db"):
        g.link_db=connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,"link_db"):
        g.link_db.close()

@app.route("/")
def main():
    db=get_db()
    movies=db.cursor().execute("SELECT title,year FROM movies")
    movies=movies.fetchall()
    return render_template("main.html",movies=movies)

@app.route("/add",methods=["POST","GET"])
def add():
    db=get_db()
    if request.method=="POST":
        title=request.form.get("title")
        year=request.form.get("year")
        if title and year:
            db.cursor().execute("INSERT INTO movies VALUES(Null,?,?)",(title,year))
            db.commit()
            flash("Данные добавлены",category="success")
        else:
            flash("Вознилка ошибка. Попробуйте еще.",category="wrong")
    return render_template("add.html")
import sqlite3 as sq
from flask import Flask, render_template,g,request, flash,redirect

DATABASE="test.db"
DEBUG=True
SECRET_KEY="1234qwert"

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
def close_db(error):
    if hasattr(g,"link_db"):
        g.link_db.close()

@app.route("/add_user", methods=["POST","GET"])
def add():
    db=get_db()
    if request.method=="POST":
        if request.form.get("name") and request.form.get("email"):
            name=request.form.get("name")
            email=request.form.get("email")
            db.cursor().execute("INSERT INTO users VALUES(Null,?,?)", (name,email))
            db.commit()  
            return redirect("/users")
    return render_template("add.html")

@app.route("/users")
def index():
    db=get_db()
    name=db.cursor().execute("SELECT name FROM users")
    result=name.fetchall()
    return render_template("index.html",names=result)
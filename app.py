from flask import Flask,g,render_template,flash,request,redirect
import sqlite3 as sq

DATABASE="tasks.db"
SECRET_KEY="1234qwer"

app=Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    conn=sq.connect(app.config["DATABASE"])
    return conn

def create_db():
    db=connect_db()
    with app.open_resource("tasks.sql",mode="r") as f:
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
def index():
    db=get_db()
    tasks=db.cursor().execute("SELECT id,description, CASE WHEN is_done='0' THEN 'НЕ ВЫПОЛНЕНО' ELSE 'Выполнено' END AS result FROM tasks").fetchall()
    return render_template("index.html",tasks=tasks)

@app.route("/add",methods=["POST","GET"])
def add():
    db=get_db()
    if request.method=="POST":
        description=request.form.get("description")
        if description:
            db.cursor().execute("INSERT INTO tasks VALUES(Null,?,?)", (description,False))
            db.commit()
            flash("Данные успешно отправлены")
        else:
            flash("Данные введены некорректно")
    return render_template("add_task.html")

@app.route("/delete/<int:task_id>", methods=["POST","GET"])
def delete(task_id):
    db=get_db()
    db.cursor().execute(f"DELETE FROM tasks WHERE id={task_id}")
    db.commit()
    return redirect("/")

@app.route("/complete/<int:task_id>")
def complete(task_id):
    db=get_db()
    db.cursor().execute(f"UPDATE tasks SET is_done='Выполнено' WHERE id={task_id}")
    db.commit()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html")

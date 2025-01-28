from flask import Flask, g, render_template, flash, request, redirect
import sqlite3 as sq
from datetime import datetime
from check_time import is_valide_date

DATABASE = "tasks.db"
SECRET_KEY = "1234qwer"

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    conn = sq.connect(app.config["DATABASE"])
    return conn


def create_db():
    db = connect_db()
    with app.open_resource("tasks.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/", methods=["POST", "GET"])
def index():
    db = get_db()
    tasks = (
        db.cursor()
        .execute(
            "SELECT id,description, CASE WHEN is_done='0' THEN 'НЕ ВЫПОЛНЕНО' ELSE 'Выполнено' END AS result, time,deadline FROM tasks ORDER BY time"
        )
        .fetchall()
    )
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST", "GET"])
def add():
    db = get_db()
    if request.method == "POST":
        description = request.form.get("description")
        deadline=request.form.get("deadline")
        if description and is_valide_date(deadline):
            db.cursor().execute(
                "INSERT INTO tasks VALUES(Null,?,?,?,?)",
                (description, False, datetime.now().strftime("%Y-%m %H:%M"),deadline),
            )
            db.commit()
            flash("Данные успешно отправлены")
        else:
            flash("Данные введены некорректно")
    return render_template("add_task.html")


@app.route("/delete/<int:task_id>", methods=["POST", "GET"])
def delete(task_id):
    db = get_db()
    db.cursor().execute(f"DELETE FROM tasks WHERE id={task_id}")
    db.commit()
    return redirect("/")




@app.route("/complete/<int:task_id>")
def complete(task_id):
    db = get_db()
    db.cursor().execute(f"UPDATE tasks SET is_done='Выполнено' WHERE id={task_id}")
    db.commit()
    return redirect("/")


@app.route("/edit/<int:task_id>", methods=["POST", "GET"])
def edit(task_id):
    db = get_db()
    form_data = request.form.to_dict()
    form_data["desc"] = (
        db.cursor()
        .execute(f"SELECT description FROM tasks WHERE id={task_id}")
        .fetchone()
    )
    if request.method == "POST":
        result = request.form.get("desc")
        if result:
            print(result)
            db.cursor().execute(
                f"UPDATE tasks SET description=? WHERE id=?", (result, task_id)
            )
            db.commit()
            return redirect("/")
        else:
            flash("ошибка")
    return render_template("edit.html", form_data=form_data, task_id=task_id)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html")

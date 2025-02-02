from flask import Flask, g, render_template, flash, request, redirect, session
import sqlite3 as sq
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from UserLogin import UserLogin
from fdatabase import FDataBase
import os


DATABASE = "tasks.db"
SECRET_KEY = os.urandom(24)

app = Flask(__name__)
app.config.from_object(__name__)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    return UserLogin().fromDB(user_id, db)


def connect_db():
    conn = sq.connect(app.config["DATABASE"])
    conn.execute("PRAGMA foreign_keys = ON")
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
    if not current_user.is_authenticated:
        return render_template("unlogin.html")

    tasks = FDataBase(db).getTask(current_user.get_id())
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST", "GET"])
@login_required
def add():
    db = get_db()
    if request.method == "POST":
        description = request.form.get("description")
        deadline = request.form.get("deadline")
        if description and deadline:
            FDataBase(db).addTask(description, deadline, current_user.get_id())
            flash("Данные успешно отправлены")
        else:
            flash("Данные введены некорректно")
    return render_template("add_task.html")


@app.route("/delete/<int:task_id>", methods=["POST", "GET"])
@login_required
def delete(task_id):
    db = get_db()
    FDataBase(db).deleteTask(task_id)
    return redirect("/")


@app.route("/complete/<int:task_id>")
def complete(task_id):
    db = get_db()
    FDataBase(db).completeTask(task_id)
    return redirect("/")


@app.route("/edit/<int:task_id>", methods=["POST", "GET"])
def edit(task_id):
    db = get_db()
    form_data = request.form.to_dict()
    desc = FDataBase(db).getDescription(task_id)
    if not desc:
        flash("Задача не найдена")
        return redirect("/")
    form_data["desc"] = desc
    if request.method == "POST":
        result = request.form.get("desc")
        new_deadline = request.form.get("new_deadline")
        if result and new_deadline:
            FDataBase(db).editTask(result, new_deadline, task_id)
            return redirect("/")
        else:
            flash("ошибка")
    return render_template("edit.html", form_data=form_data, task_id=task_id)


@app.route("/registr", methods=["POST", "GET"])
def registr():
    if current_user.is_authenticated:
        return redirect("/")
    db = get_db()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        if email and password and password == password2:
            pas = generate_password_hash(password)
            FDataBase(db).addUser(email, pas)
            return redirect("login")
        else:
            flash("Введите корректные данные")
    return render_template("registr.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    db = get_db()
    if request.method == "POST":
        user = FDataBase(db).getUser(request.form.get("email_login"))
        if not user:
            flash("Пользователь не найден")
        elif check_password_hash(user[2], request.form.get("password_login")):
            flash("Неверный пароль")
        else:
            userlogin = UserLogin().create(user)
            rm = True if request.form.get("remember") else False
            login_user(userlogin, remember=rm)
            return redirect("/")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html")

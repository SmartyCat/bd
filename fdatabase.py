from flask import flash
from datetime import datetime
import math
import sqlite3 as sq


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addTask(self, description, deadline, user_id):
        try:
            self.__cur.execute(
                "INSERT INTO tasks VALUES(Null,?,?,?,?,?)",
                (
                    description,
                    False,
                    datetime.now().strftime("%Y-%m-%d"),
                    deadline,
                    user_id,
                ),
            )
            self.__db.commit()
        except sq.DatabaseError as e:
            print("Error")
            return False

    def getTask(self, user_id):
        try:
            self.__cur.execute(
                "SELECT id,description, CASE WHEN is_done='0' THEN 'НЕ ВЫПОЛНЕНО' ELSE 'ВЫПОЛНЕНО' END AS result,time,deadline FROM tasks WHERE user_id=? ORDER BY time",
                (user_id,),
            )
            res = self.__cur.fetchall()
            return res
        except:
            return []

    def deleteTask(self, task_id):
        try:
            self.__cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            self.__db.commit()
        except sq.DatabaseError as e:
            print("Error")
            return False

    def completeTask(self, task_id):
        try:
            self.__cur.execute(
                "UPDATE tasks SET is_done='Выполнено' WHERE id=?", (task_id,)
            )
            self.__db.commit()
        except sq.DatabaseError as e:
            print(e)
            return False

    def editTask(self, result, new_deadline, task_id):
        try:
            self.__cur.execute(
                "UPDATE tasks SET description=?,deadline=? WHERE id=?",
                (result, new_deadline, task_id),
            )
            self.__db.commit()
        except sq.DatabaseError as e:
            print(e)
            return False

    def getDescription(self, task_id):
        try:
            self.__cur.execute("SELECT description FROM tasks WHERE id=?", (task_id,))
            res = self.__cur.fetchone()
            return res
        except sq.DatabaseError as e:
            print(e)

    def addUser(self, email, password):
        try:
            self.__cur.execute("INSERT INTO users VALUES(Null,?,?)", (email, password))
            self.__db.commit()
        except:
            flash("Такой логин уже существует")

    def getUser(self, email):
        try:
            res = self.__cur.execute(
                "SELECT * FROM users WHERE email=?", (email,)
            ).fetchone()
            return res
        except sq.DatabaseError as e:
            print(e)
            return False

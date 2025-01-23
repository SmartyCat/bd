from flask import Flask,g
import sqlite3 as sq 

DATABASE="test.db"
DEBUG=True
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
    if not hasattr(g,"link-db"):
        return connect_db()   

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,"link_db"):
        return connect_db().close() 
    

@app.route("/")
def index():
    return "Hello"


#! /usr/bin/python3
import cgi
import cgitb
cgitb.enable()
import sqlite3
import jinja2
import json
import hashlib
import os
def connectUsers():
    if os.name != "nt":
        mydb = sqlite3.connect('../data/users.sqlite')
    else:
        mydb = sqlite3.connect("data/users.sqlite")
    return mydb
def initdbUsers():
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER NOT NULL PRIMARY KEY,username TEXT NOT NULL, password TEXT NOT NULL, role INTEGER DEFAULT 0, email TEXT NOT NULL, friends TEXT DEFAULT [], characters TEXT DEFAULT [])")
    cnn.close()
def connectMonsters():
    mydb = sqlite3.connect('data/monsters.sqlite')
    return mydb

initdbUsers()
from http import cookies
import sys, os
form = cgi.FieldStorage()

for _name in ('stdin', 'stdout', 'stderr'):
    if getattr(sys, _name) is None:
        setattr(sys, _name, open(os.devnull, 'r' if _name == 'stdin' else 'w'))
del _name

def success(item):
    print("Content-type:text/html")
    print()
    if("action" in form):
        if form["action"].value == "get":
            cnn = connectUsers()
            cnnc = cnn.cursor()
            cnnc.execute("SELECT * FROM Users")
            result = cnnc.fetchall()
            print(json.dumps(result).replace("(","[").replace(")","]"))
        elif form["action"].value == "create":
            if "creating" in form:
                psswd = hashlib.sha3_256(str(form["psswd"].value).encode()).hexdigest()
                psswd2 = hashlib.sha3_256(str(form["psswdconf"].value).encode()).hexdigest()
                cnn = connectUsers()
                cnnc = cnn.cursor()
                if psswd2 == psswd and len(cnnc.execute("SELECT * FROM Users WHERE username = ?", (form["uname"].value,)).fetchall()) <= 0 and len(cnnc.execute("SELECT * FROM Users WHERE email = ?", (form["email"].value,)).fetchall()) <= 0:
                    cnnc.execute("""INSERT INTO Users (username,password,email,role,friends,characters) VALUES (
                        ?,?,?,?,?,?)""",(
                            form["uname"].value,
                            psswd,
                            form["email"].value,
                            form["role"].value,
                            "[]",
                            "[]"
                    ))
                    cnn.commit()
                    print('<meta http-equiv="refresh" content="0; url=/admin/users.py">')
                else:
                    print('<meta http-equiv="refresh" content="0; url=/admin/users.py#failed">')
            else:
                if os.name == "nt":
                    fle = open("admin/hide=users-create.html", "r",encoding="utf-8-sig")
                else:
                    fle = open("hide=users-create.html", "r",encoding="utf-8-sig")
                temp = jinja2.Template(fle.read())
                print(temp.render())
        elif form["action"].value == "delete":
            cnn = connectUsers()
            cnnc = cnn.cursor()
            cnnc.execute("DELETE FROM Users WHERE id = ?;", (form["id"].value,))
            cnn.commit()
            print("Ok!")


if "HTTP_COOKIE" not in os.environ:
    os.environ["HTTP_COOKIE"] = ""

roles = {"user":0,"dk":1,"dm":2,"admin":3}
if "login" in os.environ["HTTP_COOKIE"]:
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    uname = cookie["username"].value
    psswd = cookie["password"].value
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("SELECT * FROM Users WHERE username = ?", (uname,))
    result = cnnc.fetchall()
    cnn.close()
    try:
        item = result[0]
        if item[2] == psswd:
            if item[3] >= 2:
                success(item)
            else:
                assert False
        else:
            assert False
    except IndexError and AssertionError:
        print("Status-code: 303 See other")
        print("Location:/login.html")
        print("")
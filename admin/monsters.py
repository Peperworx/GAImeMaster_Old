#! /usr/bin/python3
import cgi
import cgitb
cgitb.enable()
import sqlite3
import jinja2
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

initdbUsers()
from http import cookies
import sys, os


for _name in ('stdin', 'stdout', 'stderr'):
    if getattr(sys, _name) is None:
        setattr(sys, _name, open(os.devnull, 'r' if _name == 'stdin' else 'w'))
del _name

def success(item):
    print("Content-type:text/html")
    print()
    if os.name == "nt":
        temp = jinja2.Template(open("admin/hide=monsters.html",encoding="utf-8-sig").read())
    else:
        temp = jinja2.Template(open("hide=monsters.html",encoding="utf-8-sig").read())
    print(temp.render())
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
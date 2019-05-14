#! /usr/bin/python3
import cgi
import cgitb
cgitb.enable()
import sqlite3
import jinja2
import json
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
import os
def connectMonsters():
    if os.name != "nt":
        mydb = sqlite3.connect('../data/monsters.sqlite')
    else:
        mydb = sqlite3.connect("data/monsters.sqlite")
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
        if(form["action"].value == "get"):
            cnn = connectMonsters()
            cnnc = cnn.cursor()
            cnnc.execute("SELECT * FROM Monsters")
            result = cnnc.fetchall()
            print(json.dumps(result))
        elif(form["action"].value == "delete"):
            cnn = connectMonsters()
            cnnc = cnn.cursor()
            cnnc.execute("DELETE FROM Monsters WHERE id = ?", (form["id"].value,))
            print(form["id"].value)
            cnn.commit()
        elif(form["action"].value == "create"):
            if "creating" in form:
                movement = "["+str(form["movement"].value).replace("(","[").replace(")","]")+"]"
                cnn = connectMonsters()
                cnnc = cnn.cursor()
                needed = ["name","type","ac","hd","attctype","attcdmg","noappearout","noapearin"
                        "saveas","saveaslevel","morale","treasuretype","alignment","xpval","description"]
                for item in needed:
                    if item not in form:
                        form[item].value = ""
                cnnc.execute("""INSERT INTO Monsters (name,type,ac,hd,move,attacks,appearingO,appearingD,sa,saL,morale,treasureType,alignment,xpval,description) VALUES (
                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
                    form["name"].value,
                    form["type"].value,
                    form["ac"].value,
                    form["hd"].value,
                    movement,
                    "[["+form["attctype"].value+"],["+form["attcdmg"].value+"]",
                    form["noappearout"].value,
                    form["noappearin"].value,
                    form["saveas"].value,
                    form["saveaslevel"].value,
                    form["morale"].value,
                    form["treasuretype"].value,
                    form["alignment"].value,
                    form["xpval"].value,
                    form["description"].value))
                cnn.commit()
                print('<meta http-equiv="refresh" content="0; url=/admin/monsters.py">')
            else:
                if os.name == "nt":
                    fle = open("admin/hide=monsters-create.html", "r",encoding="utf-8-sig")
                else:
                    fle = open("hide=monsters-create.html", "r",encoding="utf-8-sig")
                temp = jinja2.Template(fle.read())
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
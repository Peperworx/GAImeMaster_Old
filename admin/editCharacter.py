#! C:\Python37\python.exe
import cgi
import cgitb
cgitb.enable()
import sqlite3
import jinja2
from jinja2 import Template
import json
import hashlib
import os
if os.name == "nt":
    os.name = "wamp"
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
    itm2 = item
    if "edit" in form.keys():
        character = json.loads(form["character"].value)
        cnn = connectUsers()
        cnnc = cnn.cursor()
        id = form["uname"].value
        cnnc.execute("SELECT * FROM Users WHERE username = ?", (id,))
        result = cnnc.fetchall()
        result = result[0]
        characters = json.loads(result[6])
        i = 0
        for char in characters:
            if char["id"] == character["id"]:
                characters[i] = character
                break
            i+=1
        cnnc.execute("UPDATE Users SET characters = ? WHERE username = ?", (json.dumps(characters),id,))
        cnn.commit()
        cnn.close()
        print(f'<meta http-equiv="refresh" content="2;url=/admin/user-edit.py?id={result[0]}" />')
    else:
        cnn = connectUsers()
        cnnc = cnn.cursor()
        uid = form["uname"].value
        cnnc.execute("SELECT * FROM Users WHERE username = ?", (uid,))
        result = cnnc.fetchall()
        result = result[0]
        item = json.loads(result[6])
        for itm in item:
            if itm["id"] == form["id"].value:
                item = itm
                break
        temp = Template(open("hide=editCharacter.html").read())
        rendered = temp.render(name=item["name"],
            alignment=item["alignment"],
            clss=item["class"],
            hp=item["hp"],
            ac=item["ac"],
            strength=item["abilityScores"]["str"],
            dexterity=item["abilityScores"]["dex"],
            intelligence=item["abilityScores"]["int"],
            wisdom=item["abilityScores"]["wis"],
            constitution=item["abilityScores"]["con"],
            charisma=item["abilityScores"]["cha"],
            currency=item["currency"],
            id=item["id"],
            status=item["status"],
            xp=item["xp"],
            level=item["level"],
            inventory=item["inventory"],
            savingThrows=item["savingThrows"])
        print(rendered)


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
#! C:\Python37\python.exe
import cgi
import cgitb
cgitb.enable()
import sqlite3
import json
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

print("Content-Type: application/json\n")
cnn = connectMonsters()
cnnc = cnn.cursor()
cnnc.execute("SELECT * FROM Monsters WHERE name = ?",(form["name"].value,))
result = cnnc.fetchall()
result = json.dumps(result).replace("(","[").replace(")","]")
print(result)



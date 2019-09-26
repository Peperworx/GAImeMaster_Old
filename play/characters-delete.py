#! C:\Python37\python.exe
import cgitb
cgitb.enable()
from http import cookies
import cgi
import socket
import json
import sys
import os
import random
import hashlib
import subprocess
import sqlite3
if os.name == "nt":
    os.name = "wamp"
def connectUsers():
    if os.name != "nt":
        mydb = sqlite3.connect('../data/users.sqlite')
    else:
        mydb = sqlite3.connect('data/users.sqlite')
    return mydb
def initdbUsers():
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER NOT NULL PRIMARY KEY,username TEXT NOT NULL, password TEXT NOT NULL, role INTEGER DEFAULT 0, email TEXT NOT NULL, friends TEXT DEFAULT [], characters TEXT DEFAULT [])")
    cnn.close()

for _name in ('stdin', 'stdout', 'stderr'):
    if getattr(sys, _name) is None:
        setattr(sys, _name, open(os.devnull, 'r' if _name == 'stdin' else 'w'))
del _name
form = cgi.FieldStorage()
roles = {"user":0,"dk":1,"dm":2,"admin":3}
def success(item,uname):
    characters = json.loads(item[6])
    i=0
    for character in characters:
        if character["id"] == form["id"].value:
            del characters[i]
            break
        i+=1
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("UPDATE users SET characters = ? WHERE username = ?", (json.dumps(characters),uname,))
    cnn.commit()
    cnn.close()
    print("ContentType: text/html")
    print()
    print('<meta http-equiv="refresh" content="0; url=/play/characters.html" />')

uname = form["username"].value
cnn = connectUsers()
cnnc = cnn.cursor()
cnnc.execute("SELECT * FROM Users WHERE username = ?", (uname,))
result = cnnc.fetchall()
cnn.close()
try:
    item = result[0]
    print("Content-Type:text/html")
    print("")
    success(item,uname)
except IndexError:
    print("Content-Type:text/html\n")
    print('{"OK":"false"}')
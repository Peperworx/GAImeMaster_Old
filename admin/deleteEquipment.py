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
    mydb = sqlite3.connect('../data/users.sqlite')
    return mydb
def initdbUsers():
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER NOT NULL PRIMARY KEY,username TEXT NOT NULL, password TEXT NOT NULL, role INTEGER DEFAULT 0, email TEXT NOT NULL, friends TEXT DEFAULT [], characters TEXT DEFAULT [])")
    cnn.close()

initdbUsers()
for _name in ('stdin', 'stdout', 'stderr'):
    if getattr(sys, _name) is None:
        setattr(sys, _name, open(os.devnull, 'r' if _name == 'stdin' else 'w'))
del _name
form = cgi.FieldStorage()
roles = {"user":0,"dk":1,"dm":2,"admin":3}
def success(item):
    weapons = json.load(open("../data/equipment.json","r"))
    i=0
    
    for weapon in weapons:
        if weapon["id"] == form["id"].value:
            del weapons[i]
        i+=1
    
    json.dump(weapons,open("../data/armor.json", "r+"))
    print(open("itemAddSuccess.html","r").read())
if "HTTP_COOKIE" not in os.environ:
    os.environ["HTTP_COOKIE"] = ""

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
            print("Content-Type:text/html")
            print("")
            success(item)
        else:
            assert False
    except IndexError:
        cookie["login"]=""
        cookie["login"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
        cookie["session"]=""
        cookie["session"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
        cookie["password"]=""
        cookie["password"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
        cookie["username"]=""
        cookie["username"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
        print("Content-Type:text/html")
        print(cookie.output())
        print("")
        print ("<html><body>\n")
        print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/login.html\" />")
        print ("</body></html>")
        
else:
    cookie["login"]=""
    cookie["login"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["session"]=""
    cookie["session"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["password"]=""
    cookie["password"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["username"]=""
    cookie["username"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    print("Content-Type:text/html")
    print(cookie.output())
    print("")
    print ("<html><body>\n")
    print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/login.html\" />")
    print ("</body></html>")

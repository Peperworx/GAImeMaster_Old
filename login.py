#! /usr/bin/python3
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
def connectUsers():
    mydb = sqlite3.connect('data/users.sqlite')
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
    if "redirect" not in form:
        if item[3] > 1:
            print ("<html><body>\n")
            print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/admin\" />")
            print ("</body></html>")
            
        elif item[3] <= 1:
            print ("<html><body>\n")
            print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/play\" />")
            print ("</body></html>")
        else:
            print ("<html><body>\n")
            print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/\" />")
            print ("</body></html>")
    elif "redirect" in form:
        print ("<html><body>\n")
        print ("<meta http-equiv=\"refresh\" content=\"0; url = "+form["redirect"].value+" \/>")
        print ("</body></html>")

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
        
elif "login" not in form:
    print("Content-Type:text/html")
    print("")
    print ("<html><body>\n")
    print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/login.html\" />")
    print ("</body></html>")
elif "uname" not in form or "psswd" not in form:
    print("Content-Type:text/html")
    print("")
    print(open("loginFailed.html", "r").read())
else:
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("SELECT * FROM Users WHERE username = ?", (form["uname"].value,))
    result = cnnc.fetchall()
    cnn.close()
    try:
        item = result[0]
        if item[2] == hashlib.sha3_256(str(form["psswd"].value).encode()).hexdigest():
            print("Content-Type:text/html")
            cookie = cookies.SimpleCookie()
            cookie["session"] = random.randint(0,1000000000)
            cookie["session"]["domain"] = os.environ["HTTP_HOST"]
            cookie["username"] = form["uname"].value
            cookie["username"]["domain"] = os.environ["HTTP_HOST"]
            cookie["password"] = hashlib.sha3_256(str(form["psswd"].value).encode()).hexdigest()
            cookie["password"]["domain"] = os.environ["HTTP_HOST"]
            cookie["login"] = "login"
            cookie["login"]["domain"] = os.environ["HTTP_HOST"]
            print(cookie.output())
            print("")
            success(item)
        else:
            assert False
    except:
        print("Content-Type:text/html")
        print("")
        print(open("loginFailed.html", "r").read())

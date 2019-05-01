#! /usr/bin/python3
import cgitb
cgitb.enable()
import cgi
import socket
from http import cookies
import sys
import os
import sqlite3
def connectUsers():
    if os.name == "nt":
        mydb = sqlite3.connect('data/users.sqlite')
    else:
        mydb = sqlite3.connect('../data/users.sqlite')
    return mydb
def initdbUsers():
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER NOT NULL PRIMARY KEY,username TEXT NOT NULL, password TEXT NOT NULL, role INTEGER DEFAULT 0, email TEXT NOT NULL, friends TEXT DEFAULT [], characters TEXT DEFAULT [])")
    cnn.close()
form = cgi.FieldStorage()
def success(item):
    if os.name == "nt":
        print(open("play/hide=play.html","r").read())
    else:
        print(open("hide=play.html", "r").read())

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
            print("Status-code: 303 See Other")
            print("Location: /login.html")
            print("")
    except:
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
        print("Status-code: 303 See Other")
        print("Location:/login.html")
        print("")
else:
    print("Content-Type:text/html")
    print("Status-code: 401 Unauthorized")
    print("")
    print("You are not logged in. Please login to continue. <a href='/login.py'>Login</a>")

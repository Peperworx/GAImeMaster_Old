#! /usr/bin/python3
import cgi
import cgitb
cgitb.enable()
import socket
from http import cookies
import sys
import os
form = cgi.FieldStorage()
import sqlite3
import jinja2
def connectUsers():
    if os.name != "nt":
        mydb = sqlite3.connect('../../../data/users.sqlite')
    else:
        mydb = sqlite3.connect("data/users.sqlite")
    return mydb
def initdbUsers():
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER NOT NULL PRIMARY KEY,username TEXT NOT NULL, password TEXT NOT NULL, role INTEGER DEFAULT 0, email TEXT NOT NULL, friends TEXT DEFAULT [], characters TEXT DEFAULT [])")
    cnn.close()

initdbUsers()
def success(item):
    if os.name == "nt":
        temp = jinja2.Template(open("play/party/game/hide=playGame.html","r").read())
    else:
        temp = jinja2.Template(open("hide=playGame.html","r").read())
    if "id" in form:
        print(temp.render(id=form["id"].value))
    else:
        print ("<html><body>\n")
        print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/play/\" />")
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
    except IndexError or AssertionError:
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
    print("Content-Type:text/html")
    print("<html><body>\n")
    print("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/login.html\" />")
    print("</body></html>")

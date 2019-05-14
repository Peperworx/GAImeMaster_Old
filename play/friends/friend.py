#! /usr/bin/python3
import cgitb
cgitb.enable()
import cgi
import socket
from http import cookies
import sys
import os
form = cgi.FieldStorage()
import sqlite3
import jinja2
import json
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

def success(item):
    print("Content-Type:application/json")
    print("")
    if form["action"].value == "get":
        print(item[5].replace("'",'"'))
    elif form["action"].value == "add":
        cnn = connectUsers()
        cnnc = cnn.cursor()
        cnnc.execute("SELECT * FROM Users WHERE username=?",(form["name"].value,))
        result = cnnc.fetchall()
        if len(result) <= 0:
            print('{"ok":false}')
        else:
            item = list(item)
            item[5] = json.loads(item[5])
            item[5].append([result[0][0],form["name"].value])
            item[5] = json.dumps(item[5])
            cnnc.execute("UPDATE Users SET friends=? WHERE id=?",(item[5],item[0],))
            cnn.commit()
            print('{"ok":true}')
    elif form["action"].value == "delete":
        cnn = connectUsers()
        cnnc = cnn.cursor()
        item = list(item)
        item[5] = json.loads(item[5])
        i=0
        for itm in item[5]:
            if itm[0] == int(form["id"].value):
                del item[5][i]
                break
            i+=1
        cnnc.execute("UPDATE Users SET friends=? WHERE id=?",(json.dumps(item[5]),item[0],))
        cnn.commit()
        cnn.close()
        print('{"ok":true}')

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
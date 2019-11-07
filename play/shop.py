#! C:\Python37\python.exe
import cgitb
cgitb.enable()
import cgi
import socket
import json
from http import cookies
import sys
import os
import math
form = cgi.FieldStorage()
import sqlite3
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
def roundup(x):
    return int(math.ceil(x / 10.0)) * 10
initdbUsers()
def success(item):
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    uname = cookie["username"].value
    psswd = cookie["password"].value
    item = item
    characters =json.loads(item[6])

    itemCost = json.loads(form["item"].value)["cost"]
    itemID = json.loads(form["item"].value)["id"]
    if item[1] == uname and item[2] == psswd:
        i=0
        failed = True
        for character in characters:
            if form["charID"].value == character["id"]:
                # Do stuff to character here
                if characters[i]["currency"]["gp"] < itemCost:
                    if characters[i]["currency"]["pp"] > 0:
                        if characters[i]["currency"]["pp"] >= (roundup(itemCost) / 10):
                            charBackup = characters[i]
                            characters[i]["currency"]["pp"] -= (roundup(itemCost) / 10)
                            characters[i]["currency"]["gp"] += roundup(itemCost)
                
                if characters[i]["currency"]["gp"] < itemCost:
                    characters[i] = charBackup
                    failed = True
                else:
                    characters[i]["currency"]["gp"] -= itemCost
                    characters[i]["inventory"].append(itemID)
                    failed = False
            i+=1
        characters = json.dumps(characters)
        cnn = connectUsers()
        cnnc = cnn.cursor()
        if not failed:
            cnnc.execute("UPDATE Users SET characters = ? WHERE username = ?", (characters,uname,))
            print(json.dumps(True))
        else:
            print(json.dumps(False))
        cnn.commit()
        cnn.close()
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
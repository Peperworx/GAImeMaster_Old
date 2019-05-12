#! /usr/bin/python3
import sys
import cgi
import cgitb
import subprocess
import sqlite3
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

initdbUsers()
try:
    import psutil
except:
    subprocess.check_call([sys.executable, '-m', 'pip', "install", "psutil"])

from http import cookies
import sys, os


for _name in ('stdin', 'stdout', 'stderr'):
    if getattr(sys, _name) is None:
        setattr(sys, _name, open(os.devnull, 'r' if _name == 'stdin' else 'w'))
del _name



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
                print("Content-Type: text/html")
                print("")
                
                if os.name == "nt":
                    print(open("admin/hide=admin.html","r").read())
                else:
                    print(open("hide=admin.html", "r").read())
            else:
                print("Status: 403 Forbidden")
                print("Content-Type: text/html")
                print("")
                print("<h1>Permission denied</h1>")
                print("<p>You do not have sufficient permisions to access this resource.</p>")
                print("<p>Minimum permission level is 2.</p>")
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
        print('Status: 401 Unauthorized')
        print("Content-Type: text/html")
        print(cookie.output())
        print("")
        print ("<html><body>\n")
        print ("<h1>401 Unauthorized</h1>")
        print ("</body></html>")
else:
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    print("Content-Type: text/html")
    print("")
    cookie["login"]=""
    cookie["login"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["session"]=""
    cookie["session"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["password"]=""
    cookie["password"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["username"]=""
    cookie["username"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    print("Content-Type: text/html")
    print(cookie.output())
    print("")
    print ("<html><body>\n")
    print ("<meta http-equiv=\"refresh\" content=\"0; url = http://"+os.environ["HTTP_HOST"]+"/login.html?redirect='/admin'\" />")
    print ("</body></html>")

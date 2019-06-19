#! C:\Python37\python.exe
import cgitb
import cgi
import socket
import os
cgitb.enable()
print("Content-Type: text/html")
print("")
form = cgi.FieldStorage()
if "code" not in form:
    if os.name == "nt"
        print(open("pepperworx/main.html","r").read())
    else:
        print(open("main.html","r").read())


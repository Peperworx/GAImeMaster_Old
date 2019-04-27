#! /usr/bin/python3
import cgitb
import cgi
import socket
cgitb.enable()
print("Content-Type: text/html")
print("")
form = cgi.FieldStorage()
if "code" not in form:
    print(open("pepperworx/main.html","r").read())

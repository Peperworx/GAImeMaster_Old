#! C:\Python37\python.exe
import cgitb
import cgi
import socket
import codecs
import sys
if sys.platform == "nt":
    sys.platform = "linux"
cgitb.enable()
print("Content-Type: text/html")
print("")
form = cgi.FieldStorage()
print(open("main.html","r",encoding="utf-8-sig").read())

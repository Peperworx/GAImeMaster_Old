import cgitb
import cgi
import socket
cgitb.enable()
print("Content-Type: text/html")
print("")
form = cgi.FieldStorage()
if "code" not in form:
    print(open("main.html","r").read())

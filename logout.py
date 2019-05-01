#! /usr/bin/python3
import cgi
import cgitb
from http import cookies
import os
if "HTTP_COOKIE" in os.environ:
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    cookie["login"]=""
    cookie["login"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["session"]=""
    cookie["session"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["password"]=""
    cookie["password"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    cookie["username"]=""
    cookie["username"]["expires"]="Thu, 01 Jan 1970 00:00:00 GMT"
    print("Content-Type: text/html")
    print("Status-code: 303 See Other")
    print("Location:/")
    print(cookie.output())
    print("")
else:
    print("Content-Type: text/html")
    print("Status-code: 303 See Other")
    print("Location:/")
    print("")

#! /usr/bin/python3
import cgitb
import cgi
import socket
import codecs
cgitb.enable()
print("Content-Type: text/html")
print("")
form = cgi.FieldStorage()
print(open("main.html","r",encoding="utf-8-sig").read())

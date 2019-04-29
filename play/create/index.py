#! /usr/bin/python3
import cgitb
cgitb.enable()
import cgi
import socket
from http import cookies
import sys
import os
import subprocess
try:
	import boto3
except:
	subprocess.check_call([sys.executable, '-m', 'pip', "install", "boto3"])
form = cgi.FieldStorage()
dynamodb = boto3.resource('dynamodb', aws_access_key_id="AKIA3QPMHYLWUEZOGRW4", aws_secret_access_key="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", region_name="us-east-1")
table = dynamodb.Table('Users')
def success(item):
    if os.name == "nt":
        print(open("play/create/hide=create.html","r").read())
    else:
        print(open("hide=create.html", "r").read())

if "HTTP_COOKIE" not in os.environ:
    os.environ["HTTP_COOKIE"] = ""

if "login" in os.environ["HTTP_COOKIE"]:
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    uname = cookie["username"].value
    psswd = cookie["password"].value
    response = table.get_item(
            Key = {
                    'username':uname
                }
        )
    try:
        item = response["Item"]
        if item["password"] == psswd:
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
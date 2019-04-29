#! /usr/bin/python3
import cgitb
print("Content-type:text/html")
print()
cgitb.enable()
import cgi
import socket
from http import cookies
import sys
import os
import json
import subprocess
try:
	import boto3
except:
	subprocess.check_call([sys.executable, '-m', 'pip', "install", "boto3"])
try:
    import dice
except:
    subprocess.check_call([sys.executable,"-m","pip","install","dice"])
    import dice
form = cgi.FieldStorage()
dynamodb = boto3.resource('dynamodb', aws_access_key_id="AKIA3QPMHYLWUEZOGRW4", aws_secret_access_key="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", region_name="us-east-1")
table = dynamodb.Table('Users')
if os.name == "nt":
    cgr = json.load(open("play/create/characterGenRules.json", "r"))
else:
    cgr = json.load(open("characterGenRules.json", "r"))
if "HTTP_COOKIE" not in os.environ:
    os.environ["HTTP_COOKIE"] = ""
drc = {"fighter":"1d8","magic-user":"1d4","cleric":"1d6","theif":"1d4","dwarf":"1d8","elf":"1d6","halfling":"1d6"}
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
            savingThrows = {}
            for itm in cgr["class"]:
                if itm[0] == form["clss"].value:
                    savingThrows["PDR"] = itm[2][0]
                    savingThrows["MW"] = itm[2][1]
                    savingThrows["TSP"]= itm[2][2]
                    savingThrows["DB"]= itm[2][3]
                    savingThrows["SMS"]=itm[2][4]
            abSc = json.loads(form["abilityScores"].value)
            toAdd = {
                "abilityScores":
                {
                    "str":abSc[0],
                    "dex":abSc[1],
                    "int":abSc[2],
                    "wis":abSc[3],
                    "con":abSc[4],
                    "cha":abSc[5]
                },
                "ac":9,
                "alignment":form["align"].value,
                "class":form["clss"].value,
                "hp":sum(dice.roll(drc[form["clss"].value])),
                "inventory":[],
                "name":form["name"].value,
                "savingThrows": savingThrows
                }
            item["Characters"].append(toAdd)
            result = table.update_item(
                Key={
                    'username': uname
                },
                UpdateExpression="SET Characters = :i",
                ExpressionAttributeValues={
                    ':i': item["Characters"],
                },
                ReturnValues="UPDATED_NEW"
            )
            print(form["name"].value)
            print("Done!")
    except IndexError as e:
        print("Error!")
        print(e)
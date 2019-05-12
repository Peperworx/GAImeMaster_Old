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
    from jinja2 import Template
except:
    subprocess.check_call([sys.executable, '-m', 'pip', "install", "jinja2"])
    from jinja2 import Template
import sqlite3
def connectUsers():
    if os.name != "nt":
        mydb = sqlite3.connect('../../data/users.sqlite')
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
    import dice
except:
    subprocess.check_call([sys.executable,"-m","pip","install","dice"])
    import dice
form = cgi.FieldStorage()
if os.name == "nt":
    cgr = json.load(open("play/create/characterGenRules.json", "r"))
else:
    cgr = json.load(open("characterGenRules.json", "r"))
if "HTTP_COOKIE" not in os.environ:
    os.environ["HTTP_COOKIE"] = ""

def success(item):
    if os.name == "nt":
        temp = Template(open("play/create/hide=done.html").read())
        rendered = temp.render(name=item["name"],
            alignment=item["alignment"],
            clss=item["class"],
            hp=item["hp"],
            ac=item["ac"],
            strength=item["abilityScores"]["str"],
            dexterity=item["abilityScores"]["dex"],
            intelligence=item["abilityScores"]["int"],
            wisdom=item["abilityScores"]["wis"],
            constitution=item["abilityScores"]["con"],
            charisma=item["abilityScores"]["cha"])
        print(rendered)
    else:
        temp = Template(open("hide=done.html").read())
        rendered = temp.render(name=item["name"],
            alignment=item["alignment"],
            clss=item["class"],
            hp=item["hp"],
            ac=item["ac"],
            strength=item["abilityScores"]["str"],
            dexterity=item["abilityScores"]["dex"],
            intelligence=item["abilityScores"]["int"],
            wisdom=item["abilityScores"]["wis"],
            constitution=item["abilityScores"]["con"],
            charisma=item["abilityScores"]["cha"])
        print(rendered)

drc = {"fighter":"1d8","magic-user":"1d4","cleric":"1d6","theif":"1d4","dwarf":"1d8","elf":"1d6","halfling":"1d6"}
if "login" in os.environ["HTTP_COOKIE"]:
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    uname = cookie["username"].value
    psswd = cookie["password"].value
    cnn = connectUsers()
    cnnc = cnn.cursor()
    cnnc.execute("SELECT * FROM Users WHERE username = ?", (uname,))
    result = cnnc.fetchall()
    try:
        item = result[0]
        if item[2] == psswd:
            savingThrows = {}
            for itm in cgr["class"]:
                if itm[0] == form["clss"].value:
                    savingThrows["PDR"] = itm[2][0]
                    savingThrows["MW"] = itm[2][1]
                    savingThrows["TSP"]= itm[2][2]
                    savingThrows["DB"]= itm[2][3]
                    savingThrows["SMS"]=itm[2][4]
            abSc = json.loads(form["abilityScores"].value)
            hp = sum(dice.roll(drc[form["clss"].value]))
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
                "hp":hp,
                "inventory":[],
                "name":form["name"].value,
                "savingThrows": savingThrows
                }
            charactersL = item[6]
            charactersL = json.loads(charactersL)
            charactersL.append(toAdd)
            charactersL = json.dumps(charactersL)
            cnnc.execute("UPDATE Users SET characters = ? WHERE username=?", (charactersL,uname,))
            cnn.commit()
            success(toAdd)
    except KeyboardInterrupt as e:
        print("Error!")
        print(e)
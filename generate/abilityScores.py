#! C:\Python37\python.exe
import json
import subprocess
import cgi
import cgitb
import sys
cgitb.enable()
"""
try:
	import dice
except:
	subprocess.check_call([sys.executable, '-m', 'pip', "install", "dice"])
	import dice
"""
import dice

print("Content-Type:application/json")
print()
rolls = [sum(dice.roll("3d6")),sum(dice.roll("3d6")),sum(dice.roll("3d6")),sum(dice.roll("3d6")),sum(dice.roll("3d6")),sum(dice.roll("3d6"))]
print(json.JSONEncoder().encode(rolls))
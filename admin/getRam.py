#! /usr/bin/python3
import cgi
print("Content-Type: application/json")
print()
import cgitb
import sys
cgitb.enable()
import subprocess
try:
    import psutil
except:
    subprocess.check_call([sys.executable, '-m', 'pip', "install", "psutil"])
print(psutil.virtual_memory().percent)
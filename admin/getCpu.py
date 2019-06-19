#! C:\Python37\python.exe
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
print(psutil.cpu_percent(interval=1, percpu=True))
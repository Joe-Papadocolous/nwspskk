#Version: 1.2

import subprocess
import re
import os

# gets name of pc and username
pc_name = os.getenv('COMPUTERNAME')
username = os.getlogin()

# gets names of all previously connected networks
profiles = subprocess.check_output("netsh wlan show profile")
profiles = profiles.decode("utf-8")
a_profiles = profiles.split("\r\n    All User Profile     : ")
a_profiles.pop(0)
last = a_profiles.pop(-1)
last = last.replace("\r\n\r\n", "")
a_profiles.append(last)

the_list = ""

# gets passwords of each network
for i in a_profiles:
    try:
        pswd = subprocess.check_output(f'netsh wlan show profile "{i}" key=clear')
        pswd = pswd.decode("utf-8")
        result = re.search("Key Content            : (.*)\r\n\r\nCost settings", pswd)
        string = ("Network name: " + i + "\nNetwork password: " + result.group(1) + "\n\n")
        the_list = the_list + string
    except:
        string = ("Network name: " + i + "\nError retrieving password\n\n")
        the_list = the_list + string

name = pc_name + "_" + username + "_networkinfo.txt"

# ouputs results to .txt file
with open(name, "w") as file:
    file.write(the_list)

# opens the notepad document
subprocess.Popen(["notepad.exe", name])

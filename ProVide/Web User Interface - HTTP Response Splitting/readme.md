# SetLanguage 

## Summary

The application does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to HTTP Response Splitting.

## VulDB-Like Summary

A vulnerability has been found in the Admin Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1. It has been declared as problematic. Affected by this vulnerability is an unknown part of the file /ajax/GetInheritedProperties. The manipulation of the parameter **language** with the input value `%0d%0a` leads to a HTTP Response Splitting vulnerability. The CWE definition for the vulnerability is CWE-113. As an impact it is known to affect integrity. An attacker may be able to insert a newline character to split a header, and inject malicious content to deceive site visitors.

The weakness was disclosed 04/06/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2020-XXXX. The attack can be launched remotely. The exploitation doesn't need any form of authentication. Technical details of the vulnerability are known, but there is no available exploit.

## Proof-of-Concept

**Sample affected URLs:**

* https://provide.ftp.local:8443/dkb4QRBT4hG4EGMu/ajax/setlanguage

## Remediation

No official fix has been released to fix this issue.

## References

* [https://cwe.mitre.org/data/definitions/113.html](https://cwe.mitre.org/data/definitions/113.html)
* [https://owasp.org/www-community/attacks/HTTP_Response_Splitting](https://owasp.org/www-community/attacks/HTTP_Response_Splitting)

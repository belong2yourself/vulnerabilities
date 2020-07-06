# Index.php Reflected Cross-Site-Scripting

## Summary

The application does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Reflected Cross-Site Scripting.

A vulnerability was found in Codemagic Sitemagic CMS 4.4.1 (Content Management System). It has been declared as problematic. Affected by this vulnerability is an unknown part of the file /sitemagic/index.php. The manipulation with the input value /'-alert(document.cookie)-'a/b/c/ leads to a cross site scripting vulnerability. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. An attacker might be able to inject arbitrary html and script code into the web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

The weakness was disclosed 10/21/2019 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2019-18219. The attack can be launched remotely. The exploitation doesn't need any form of authentication. Technical details of the vulnerability are known, but there is no available exploit.

## Proof-of-Concept

**Sample affected URL:**

* http://[Hostname]/'-alert(document.cookie)-'a/b/c/
* http://[Hostname]/upgrade.php?UpgradeMode=%3Cscript%3Ealert(document.cookie)%3C%2fscript%3E

## Remediation

Upgrading to version 4.4.2 eliminates this vulnerability.

## References

* https://www.owasp.org/index.php/Cross-site_Scripting_(XSS) 
* https://www.google.com/intl/en/about/appsecurity/learning/xss/ 
* https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet 

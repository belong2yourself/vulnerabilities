# GetInheritedProperties - Reflected Cross-Site-Scripting via "groups" parameter manipulation

## Summary

The application does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Reflected Cross-Site Scripting.

## VulDB-Like Summary

A vulnerability has been found in the Admin Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1. It has been declared as problematic. Affected by this vulnerability is an unknown part of the file /ajax/GetInheritedProperties. The manipulation of the parameter **groups** with the input value `%5B<svg+onload="javascript:alert(1)">%5D` leads to a cross site scripting vulnerability. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. An attacker might be able to inject arbitrary html and script code into the web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

The weakness was disclosed 04/06/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2020-XXXX. The attack can be launched remotely. The exploitation doesn't need any form of authentication. Technical details of the vulnerability are known, but there is no available exploit.

## Proof-of-Concept

**Sample affected URL:**

* https://provide.ftp.local:8443/ajax/GetInheritedProperties

## Remediation

No official fix has been released to mitigate this vulnerability.

## References

* https://www.owasp.org/index.php/Cross-site_Scripting_(XSS) 
* https://www.google.com/intl/en/about/appsecurity/learning/xss/ 
* https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet 

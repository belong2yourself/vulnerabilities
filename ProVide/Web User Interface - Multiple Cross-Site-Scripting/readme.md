# Web Admin Interface - Multiple Cross-Site-Scripting

## Summary

The User Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1 does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Multiple Stored and Reflected Cross-Site Scripting.

Affected by this vulnerability are multiple endpoints of the Web Admin Interface, and multiple parameters. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. An attacker might be able to inject arbitrary html and script code into the user accessible web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

For further details, refer to the singles vulnerabilities.

* [Collaborate - Reflected](./Collaborate - Reflected Cross-Site Scripting)
* [Collaborate - Stored](./Collaborate - Stored Cross-Site Scripting)
* [Deletemultiple - Reflected](./Deletemultiple - Reflected Cross-Site Scripting)
* [Share - Reflected](./Share - Reflected Cross-Site Scripting)
* [Share - Stored](./Share - Stored Cross-Site Scripting)
* [Waitedit - Reflected](./Waitedit - Reflected Cross-Site Scripting)

## Remediation

No official fix has been released to mitigate this vulnerability.

## References

* [https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)) 
* [https://www.google.com/intl/en/about/appsecurity/learning/xss/](https://www.google.com/intl/en/about/appsecurity/learning/xss/)
* [https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet](https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet) 

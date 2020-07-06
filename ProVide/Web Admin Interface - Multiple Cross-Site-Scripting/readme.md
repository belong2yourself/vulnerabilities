# Web Admin Interface - Multiple Cross-Site-Scripting

## Summary

The Admin Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1 does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Multiple Stored and Reflected Cross-Site Scripting.

Affected by this vulnerability are multiple endpoints of the Web Admin Interface, and multiple parameters. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. This vulnerability is handled as CVE-2020-11704.
An attacker might be able to inject arbitrary html and script code into the user accessible web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

For further details, refer to the single vulnerabilities.

* [SetUserInfo](https://github.com/belong2yourself/vulnerabilities/tree/master/ProVide/Web%20Admin%20Interface%20-%20Multiple%20Cross-Site-Scripting/GetInheritedProperties%20-%20Reflected%20Cross-Site%20Scripting)
* [GetUserInfo](https://github.com/belong2yourself/vulnerabilities/tree/master/ProVide/Web%20Admin%20Interface%20-%20Multiple%20Cross-Site-Scripting/GetUserInfo%20-%20Reflected%20Cross-Site%20Scripting)
* [GetInheritedProperties](https://github.com/belong2yourself/vulnerabilities/tree/master/ProVide/Web%20Admin%20Interface%20-%20Multiple%20Cross-Site-Scripting/SetUserInfo%20-%20Stored%20Cross-Site%20Scripting)

## Remediation

No official fix has been released to mitigate this vulnerability.

## References

* [https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)) 
* [https://www.google.com/intl/en/about/appsecurity/learning/xss/](https://www.google.com/intl/en/about/appsecurity/learning/xss/)
* [https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet](https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet) 

# Multiple Cross-Site-Scripting

## Summary

MonoX CMS for .NET up to v5.1.40.5152 does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Multiple Stored Cross-Site Scripting. Both the admin area and the user area allows for this kind of attack. However, as the admin area allows for direct HTML modification, the whole application is "vulnerable" by design. As such, the scope of the research was restricted to the user area, in input fields which should not allow HTML tags.

Affected by this vulnerability are multiple endpoints of both the Admin and User web UI, and multiple parameters. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. This vulnerability is handled as CVE-2020-XXXX. 
An attacker might be able to inject arbitrary html and script code into the user accessible web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

For further details, refer to the single vulnerabilities.

* [User Status](https://github.com/belong2yourself/vulnerabilities/tree/master/MonoX%20CMS/Multiple%20Cross-Site-Scripting/User%20Status%20-%20Stored%20Cross-Site-Scripting)
* [Blog Comments](https://github.com/belong2yourself/vulnerabilities/tree/master/MonoX%20CMS/Multiple%20Cross-Site-Scripting/Blog%20Comments%20-%20Stored%20Cross-Site-Scripting)
* [Blog Description](https://github.com/belong2yourself/vulnerabilities/tree/master/MonoX%20CMS/Multiple%20Cross-Site-Scripting/Blog%20Description%20-%20Stored%20Cross-Site-Scripting)

## Remediation

No official fix has been released to mitigate this vulnerability.

## References

* [https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)) 
* [https://www.google.com/intl/en/about/appsecurity/learning/xss/](https://www.google.com/intl/en/about/appsecurity/learning/xss/)
* [https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet](https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet) 

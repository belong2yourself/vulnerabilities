---
layout: default
parent: ProVide FTP Server for Windows
nav_order: 2
title: CVE-2020-11702 - Multiple XSS in Web User Interface
has_children: true
---

# Web User Interface - Multiple Cross-Site-Scripting

## Summary

The User Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1 does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Multiple Stored and Reflected Cross-Site Scripting.

Affected by this vulnerability are multiple endpoints of the Web Admin Interface, and multiple parameters. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. This vulnerability is handled as CVE-2020-11702. 
An attacker might be able to inject arbitrary html and script code into the user accessible web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

For further details, refer to the single vulnerabilities.

## Remediation

Update the software to v14.0 or higher solves the issue.

## References

* [https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)) 
* [https://www.google.com/intl/en/about/appsecurity/learning/xss/](https://www.google.com/intl/en/about/appsecurity/learning/xss/)

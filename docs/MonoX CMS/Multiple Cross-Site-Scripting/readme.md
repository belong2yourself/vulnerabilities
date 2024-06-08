---
layout: default
parent: MonoX CMS
nav_order: 1
title: CVE-2020-12472 - Multiple Cross-Site-Scripting
has_children: true
---

# Multiple Cross-Site-Scripting

## Summary

MonoX CMS for .NET up to v5.1.40.5152 does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Multiple Stored Cross-Site Scripting. Both the admin area and the user area allows for this kind of attack. However, as the admin area allows for direct HTML modification, the whole application is "vulnerable" by design. As such, the scope of the research was restricted to the user area, in input fields which should not allow HTML tags.

Affected by this vulnerability are multiple endpoints of both the Admin and User web UI, and multiple parameters. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. This vulnerability is handled as CVE-2020-12472. 
An attacker might be able to inject arbitrary html and script code into the user accessible web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

For further details, refer to the single vulnerabilities.

## Remediation

No official fix has been released to mitigate this vulnerability.

## References

* [OWASP - Cross-site Scripting](https://owasp.org/www-community/attacks/xss/) 
* [OWASP - XSS - Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) 

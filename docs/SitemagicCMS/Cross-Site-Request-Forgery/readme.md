---
layout: default
title: CVE-2019-18220 - Cross-Site-Request-Forgery (CSRF)
nav_order: 1
parent: Sitemagic CMS
---

# Cross-Site-Request-Forgery (CSRF)

## Summary

A vulnerability was found in Codemagic Sitemagic CMS 4.4.1 (Content Management System). It has been rated as problematic. Affected by this issue is an unknown code. The manipulation with an unknown input leads to a cross site request forgery vulnerability. Using CWE to declare the problem leads to CWE-352. Impacted is integrity. An attacker might be able force legitimate users to initiate unwanted actions within the web application.

The weakness was presented 10/21/2019 by Alessandro Magnosi (deadc0de) (GitHub Repository). The advisory is shared for download at github.com. This vulnerability is handled as CVE-2019-18220. The attack may be launched remotely. No form of authentication is required for exploitation. There are neither technical details nor an exploit publicly available.

## Proof-of-Concept

The following PoC can be used to create a file under C:\Users\Public\Document [Replace depending on installation type]. 

**Steps to reproduce:**

A [proof-of-concept](https://github.com/belong2yourself/vulnerabilities/blob/master/docs/SitemagicCMS/Cross-Site-Request-Forgery/csrf-poc.html) code has been provided, and can be used to create a web shell on the root directory of the server. 

Steps to reproduce:

1.  Clone the csrf-poc.html file
2.  Modify in the PoC the target references:
  a.  var target = <ip or hostname>;
  b.  var sitemagic = <sitemagic path>;
3.  Login as admin into Sitemagic CMS web application
4.  Open the file with the browser in a new tab
5.  Access the web-shell on http[s]://hostname/sitemagic/simple-shell.php

Note: the following PoC has been tested on Google Chrome with web security disabled (Needed to avoid XHR issues).

## Remediation

Upgrading to version 4.4.2 eliminates this vulnerability.

## References

*	[https://owasp.org/www-community/attacks/csrf](https://owasp.org/www-community/attacks/csrf) 



 

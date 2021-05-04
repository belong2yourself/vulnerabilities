---
layout: default
grand_parent: ProVide FTP Server for Windows
nav_order: 1
parent: CVE-2020-11702 - Multiple XSS in Web User Interface
title: Stored XSS in /ajax/share
---

# Share - Stored Cross-Site-Scripting via "displayname" parameter manipulation

## Summary

The application does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Stored Cross-Site Scripting.

In the context of this vulnerability, a logged in attacker may execute active content in the context of other logged in users, injecting JavaScript or other active contect in the display name, and sharing a public accessible link.

## VulDB-Like Summary

A vulnerability has been found in the Admin Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1. It has been declared as problematic. Affected by this vulnerability is an unknown part of the file /ajax/share. The manipulation of the parameter **displayname** with the input value `%5B%22%2F<svg+onload=alert(1)>%22%5D` leads to a cross site scripting vulnerability. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. An attacker might be able to inject arbitrary html and script code into the web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

The weakness was disclosed 04/06/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2020-11702. The attack can be launched remotely. The exploitation doesn't need any form of authentication. Technical details of the vulnerability are known, but there is no available exploit.

## Proof-of-Concept

**Sample affected URL:**

* https://provide.ftp.local:8443/dkb4QRBT4hG4EGMu/ajax/share

**Affected Parameter:**

* `displayname`

## Remediation

Updating the software to v14.0 or higher should solve the issue.

## References

* [https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS))
* [https://www.google.com/intl/en/about/appsecurity/learning/xss/](https://www.google.com/intl/en/about/appsecurity/learning/xss/) 

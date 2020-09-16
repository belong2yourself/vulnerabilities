---
layout: default
grand_parent: MonoX CMS
nav_order: 2
parent: CVE-2020-12472 - Multiple Cross-Site-Scripting
title: Sored XSS in Blog Description 
---
# Blog Description - Stored Cross-Site-Scripting via txtDescription parameter

## Summary

The application does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Stored Cross-Site Scripting.

In the context of this vulnerability, a logged in attacker may execute active content in the context of other logged in users, injecting JavaScript or other active contect in the display name, and sharing a public accessible link.

## VulDB-Like Summary

A vulnerability has been found in MonoX CMS for .NET up to v5.1.40.5152. It has been declared as problematic. Affected by this vulnerability is an unknown part of the file `MonoX.MonoSoftware.MonoX.ModuleGallery.Blog.BlogPostEdit`. The manipulation of the parameter **ctl00$cp$gridViewBox$ctlBlogSettings$txtDescription** with the input value `<audio+src+onloadstart=alert(1)>` leads to a cross site scripting vulnerability. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect integrity. An attacker might be able to inject arbitrary html and script code into the web site. This would alter the appearance and would make it possible to initiate further attacks against site visitors.

The weakness was disclosed 04/21/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2020-12472. The attack can be launched remotely. The exploitation doesn't need any form of authentication. Technical details of the vulnerability are known, but there is no available exploit.

## Proof-of-Concept

**Sample affected URL:**

* http://monox.local/MonoX/Admin/BlogSettingsManager/posts/[post-title]/

**Affected Parameter:**

* `txtDescription`

## Remediation

No official fix is available for this issue.

## References

* [https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS))
* [https://www.google.com/intl/en/about/appsecurity/learning/xss/](https://www.google.com/intl/en/about/appsecurity/learning/xss/) 
* [https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet](https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet) 

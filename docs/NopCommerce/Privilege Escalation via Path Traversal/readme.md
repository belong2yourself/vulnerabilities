---
layout: default
parent: NopCommerce Shopping CMS
nav_order: 3
title: CVE-2019-19684 - Privilege Escalation via Path Traversal
---

# Privilege Escalation via Path Traversal

## Summary

It was found that the implementation of the file manager “RoxyFileman”, shipped with NopCommerce v4.2.0 is vulnerable to path traversal attacks. A Path Traversal attack aims to access files and directories that are stored outside the web root folder by manipulating variables that reference files with “dot-dot-slash (../)” sequences and its variations.  This can allow an attacker to access arbitrary files and directories stored on file system, including application source code, configuration and critical system files. Using the uploaded files, it is hence possible to achieve code execution on the server. 

Affected are all the functionalities of the file Libraries/Nop.Services/Media/RoxyFileman/FileRoxyFilemanService.cs. The manipulation of the URL parameters "d" [directory], "f" [file] with arbitrary relative paths leads to the possibility to download, upload, rename or move files and directories within the server filesystem, and can lead to remote command execution on the underlying server. CWE is classifying the issue as CWE-23. This is going to have an impact on confidentiality, integrity, and availability.

The weakness was discovered during June 2019 by Alessandro Magnosi and Jun Woo Lee and it is uniquely identified as CVE-2019-19684. The exploitability is told to be non-trivial. It is possible to launch the attack remotely. A single authentication is necessary for exploitation. Technical details are known, and a public exploit has been developed by Alessandro Magnosi and released to the public.

The weaponized version of the exploit permits to upload a Web Shell overwriting a default file of the CMS. 

## Proof-of-Concept

During the review, it was possible for an administrator user to exploit the RoxyFileman file upload functionality to read and write arbitrary files on the server. This behavior could be exploited to modify critical application server files, achieving code execution on the machine. 

**Sample affected URL:**

*	http://[HOSTNAME]/Admin/RoxyFileman/ProcessRequest?a=DOWNLOAD&f=%2Fimages%2Fuploaded%2Fuploaded2%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd (Read)
*	http://[HOSTNAME]/Admin/RoxyFileman/ProcessRequest?a=UPLOAD (Write)

To reproduce the issue, the following steps can be used:

*	Install the docker version of NopCommerce
*	Change [HOSTNAME] in the PoC URLs to the IP/Hostname of the docker appliance
*	Login in the application as an administrator
*	Navigate to the first link
*	The file passwd will be downloaded as a regular file

To ease the exploitation, an [exploit script](https://github.com/belong2yourself/vulnerabilities/blob/master/docs/NopCommerce/Privilege%20Escalation%20via%20Path%20Traversal/privesc-pat-trav.py) has been provided, which can be used against a vulnerable version of the CMS to upload a Web Shell, overwrite the "Contact Us" page. The uploaded Web Shell is a specially crafted .NET MVC Shell, using Razor syntax.

## Remediation

Upgrading to version 4.3.0 solves the issue.
The official fix is been implemented in the following commit:
[Refactoring RoxyFileman Functions](https://github.com/nopSolutions/nopCommerce/commit/7d9f4bf5b8de15c5828043ac7005bc7bef2a9544#diff-e4dd0547abf79ee1f78cd588f908e682)

## References

*	https://www.owasp.org/index.php/Path_Traversal 
*	https://www.acunetix.com/websitesecurity/directory-traversal/

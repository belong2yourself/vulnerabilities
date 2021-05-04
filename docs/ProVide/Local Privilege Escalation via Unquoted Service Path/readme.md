---
layout: default
parent: ProVide FTP Server for Windows
nav_order: 9
title: LPE via Unquoted-Service-Path
---

# Local Privilege Escalation via Unquoted Service Path

## Summary

It was identified that ProVide FTP Server (formerly zFTP) for Windows, is installed using an Unquoted Service Path, and it runs with Local System Privileges. A local, unprivileged attacker can abuse this condition to escalate her priviliges to Local System.

## VulDB-Like Summary

A vulnerability has been found in ProVide FTP Server (formerly zFTP) for Windows up to 13.1 and classified as critical. This vulnerability affects some unknown functionality. The manipulation with an unknown input leads to a privilege escalation vulnerability. The CWE definition for the vulnerability is CWE-428. As an impact it is known to affect confidentiality, integrity, and availability.

The weakness was shared 04/08/2020 by deadc0de (GitHub Repository). The attack needs to be approached locally. A single authentication is needed for exploitation. Technical details are known but there is no exploit publicly available.  

## Proof-of-Concept

The service is installed using an Unquoted-Service-Path:

```shell
PS C:\Users\IEUser> gwmi -class Win32_Service -Property Name, DisplayName, PathName, StartMode | Where {$_.StartMode -eq "Auto" -and $_.PathName -notlike "C:\Windows*" -and $_.PathName -notlike '"*'} | select PathName,DisplayName,Name

PathName                                            DisplayName                Name
--------                                            -----------                ----
C:\Program Files (x86)\ProVide\ProVide.exe /service ProVide integration server ProVideSvc
```

The service then runs with Local System privileges:

```shell
PS C:\Users\IEUser> tasklist /V | findstr /i provide.exe
ProVide.exe                   5604 Services                   0     20,252 K Unknown         NT AUTHORITY\SYSTEM
                             0:00:01 N/A
```

## Remediation

Updating the software to v14.0 or higher should solve the issue.

## References

* [https://cwe.mitre.org/data/definitions/428.html](https://cwe.mitre.org/data/definitions/428.html)
* [https://cwe.mitre.org/data/definitions/269.html](https://cwe.mitre.org/data/definitions/269.html)
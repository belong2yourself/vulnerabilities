# Web Admin Interface - Authenticated Path Traversal

## Summary

The application allows the FTP server admin to execute programs upon eventsdoes not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Path Traversal, leading to arbitrary file overwrite. 

The applicatio doesn't adequately check the certificate filename during the import routine. That could be used by an attacker to load an arbitrary certificate in `.pfx` format wherever in the filesystem. Moreover, the application fails to neutralise NULL bytes, allowing then an attacker to have full control over the file path and name. Using the payload `../../../../pwnd.exe%00`, an executable file is created under `C:\`.

## VulDB-Like Summary

A vulnerability has been found in the Admin Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1. It has been declared as critical. Affected by this vulnerability is an unknown part of the file /ajax/ImportCertificate. The manipulation of the parameter **fileName** with `../` and `%00` leads to a path traversal vulnerability. The CWE definition for the vulnerability is CWE-23. As an impact it is known to affect integrity and availability. An attacker might be able to overwrite arbitrary files on the filesystem, corrupting them.

The weakness was disclosed 05/06/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). It is possible to read the advisory at github.com. This vulnerability is known as CVE-2020-XXXX. The attack can be launched remotely. A single authentication is needed for exploitation. Technical details of the vulnerability are known, and a public exploit has been released to the public.

## Proof-of-Concept

The `overwrite.py` script has been provided to reproduce the issue. If used on a fresh installation of the product, which means: 

* no users exists (except for 1 admin) 
* no direct filesystem access is granted to anyone, not even to admin
* HTTP/HTTPS filesystem access is not enabled

The script could still create a file called **pwnd.exe** under the `C:\` directory.

```shell
root@kali:~# python3 overwrite.py -t 192.168.226.140 -u Admin -p Passw0rd! 
[+] Logging in
[+] Creating Evil File:
[+] Done! Check the filesystem!
```

## Remediation

Currently, no official fix is available for this issue.

## References

* [https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A5-Broken_Access_Control](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A5-Broken_Access_Control)
* [https://www.acunetix.com/blog/web-security-zone/what-is-privilege-escalation/](https://www.acunetix.com/blog/web-security-zone/what-is-privilege-escalation/)
* [https://cwe.mitre.org/data/definitions/269.html](https://cwe.mitre.org/data/definitions/269.html)

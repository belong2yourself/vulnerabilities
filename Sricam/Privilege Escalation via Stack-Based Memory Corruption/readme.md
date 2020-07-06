# Code Execution via Stack-Based Memory Corruption

## Summary

It was found that Sricam Device Viewer, a device management interface for IP CCTV Cameras by Sricam, is vulnerable to a stack-based memory corruption. A stack-based memory corruption, buffer overflow, or buffer overrun, is an anomaly where a program, while writing data to a buffer, overruns the buffer's boundary and overwrites adjacent memory locations. This vulnerability could be exploited to trigger a denial-of-service condition, or to execute arbitrary code, eventually achieving a local privilege escalation.

Affected by the functionality is the field "username" of the add-user functionality. The manipulation of the user parameter with a crafted payload leads to the possibility to overwrite arbitrary memmory locations, and can lead to code execution on the underlying server.

The weakness was discovered during October 2019.

## Proof-of-Concept

During the review, it was possible for a low privileged user to exploit the Sricam Device Viewer add-user functionality to execute code in the context of the owner of DeviceViewer.exe process.

Steps to reproduce:

1. Get the WinExec address from arwin.exe kernel32.dll WinExec
2. Change the related address in the PoC
3. Generate the payload using the PoC
4. Log in the Sricam DeviceViewer application
5. Go to System Configuration -> User Management
6. Put the content of the generated file in User Info -> Username  
7. Click on Add
8. A command shell will appear

## Remediation

No fix has been released or planned to be released for this vulnerability. 

## References

* [https://owasp.org/www-community/vulnerabilities/Buffer_Overflow](https://owasp.org/www-community/vulnerabilities/Buffer_Overflow)
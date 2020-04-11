# Arbitrary Password Change via Stack-Based Memory Corruption

## Summary

It was found that Sricam Device Viewer, a device management interface for IP CCTV Cameras by Sricam, is vulnerable to a stack-based memory corruption. A stack-based memory corruption, buffer overflow, or buffer overrun, is an anomaly where a program, while writing data to a buffer, overruns the buffer's boundary and overwrites adjacent memory locations. This vulnerability could be exploited to trigger a denial-of-service condition, execute arbitrary code, or alter the original flow of the program causing unexpected behaviours.

Affected by the vulnerability is the field "old password" of the change-password functionality. The manipulation of the password parameter with a crafted payload leads to the possibility to alter the flow of the program and to change the current user password with a new one, without possessing the old password.

The bug was discovered during October 2019. 

## Proof-of-Concept

During the review, it was possible for a logged-in user to use the change password functionality to change the current password bypassing the old password check.

Steps to reproduce:
    
1. Generate the payload executing the PoC
2. Login in the Sricam DeviceViewer application as any registered user
3. Go to System Tools -> Change Password
4. Set the old password as the malicious payload, and the new password as whatever you want
5. The password will be changed with the new one
6. To confirm, restart the application and try to login with the new password

## Remediation

No fix has been released or planned to be released for this vulnerability. 

## References

* [https://owasp.org/www-community/vulnerabilities/Buffer_Overflow](https://owasp.org/www-community/vulnerabilities/Buffer_Overflow)
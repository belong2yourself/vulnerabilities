---
layout: default
nav_order: 1
parent: Foscam VMS
title: UID Denial-of-Service
---
# Foscam UID Denial-of-Service

## Summary

It was found that Foscam VMS, a device management interface for IP CCTV Cameras by Foscam, is vulnerable to a memory corruption. A memory corruption, buffer overflow, or buffer overrun, is an anomaly where a program, while writing data to a buffer, overruns the buffer's boundary and overwrites adjacent memory locations. This vulnerability could be exploited to trigger a denial-of-service condition, execute arbitrary code, or alter the original flow of the program causing unexpected behaviours.

Affected by the vulnerability is the field "uid" of the add P2P device functionality. The manipulation of the UID parameter with a crafted payload leads to a denial-of-service (DOS) condition. 

The weakness was discovered during October 2019.

## Proof-of-Concept

During the review, it was possible for a logged-in user to crash the program.

Steps to Produce the Crash: 

1. Run python code : python foscam-vms-uid-dos.py
2. Open FoscamVMS1.1.6.txt and copy its content to clipboard
3. Open FoscamVMS
4. Go to Add Device
5. Check the option P2P Connection
6. Copy the content of the file into UID
7. Click on Login Check
8. Crashed

## Remediation

No fix has been released or planned to be released for this bug. 

## References

* [https://owasp.org/www-community/vulnerabilities/Buffer_Overflow](https://owasp.org/www-community/vulnerabilities/Buffer_Overflow)
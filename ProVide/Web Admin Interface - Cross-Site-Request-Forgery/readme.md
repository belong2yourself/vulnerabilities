# Web Admin Interface - Cross-Site-Request-Forgery (CSRF)

## VulDB-Like Summary

A vulnerability has been found in the User Web Interface of ProVide FTP Server (formerly zFTP) for Windows up to v13.1. It has been rated as problematic. Affected by this issue is an unknown code. The manipulation with an unknown input leads to a cross site request forgery vulnerability. Using CWE to declare the problem leads to CWE-352. Impacted is integrity. An attacker might be able force legitimate users to initiate unwanted actions within the web application.

The weakness was presented 04/08/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). The advisory is shared for download at github.com. This vulnerability is handled as CVE-2020-XXXX. The attack may be launched remotely. No form of authentication is required for exploitation. Technical details are known and a proof-of-concept exploit is publicly available.

## Proof-of-Concept

**Sample affected URLs:**

All the Admin Interface is vulnerable to this kind of issue, which can be leveraged to trick an admin user in performing the following actions, among others:

* Change any username and password, admin ones included 
* Create/Delete users
* Enable/Disable Services
* Set a rogue update proxy
* Shutdown the server

As a proof-of-concept, an HTML/Javascript PoC was created, that can be used to create a new FTP user in the server. 

**Steps to reproduce:**

1.  Clone the csrf-poc.html file
2.  Modify in the PoC the target references:
  a.  var target = <ip or hostname>;
3.  Login as admin into ProVide FTP Server - Web Admin Interface
4.  Open the file with the browser in a new tab
5.  See the new user abcdefghi created

## Remediation

Currently, no fixes are available for this issue.

## References

*	https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF) 
*	https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet 



 

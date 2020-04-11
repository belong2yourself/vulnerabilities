# Privilege Escalation via unprotected Plugin Upload

## Summary

It was identified that NopCommerce v4.2.0 was affected by a privilege escalation via file upload as it fails to adequately analyse uploaded files. This can allow the upload of malicious files, such as malware, web-shells or other executable code. An attacker who uploads files of this nature can compromise the underlying application server.

Affected are all the functionalities of the file Presentation/Nop.Web/Admin/Areas/Controllers/PluginController.cs. The manipulation of a plugin with arbitrary files leads to remote command execution on the underlying server. CWE is classifying the issue as CWE-269. This is going to have an impact on confidentiality, integrity, and availability.

The weakness was discovered during December 2019 and it is uniquely identified as CVE-2019-19684 since 12/09/2019. The exploitability is told to be trivial. It is possible to launch the attack remotely. A single authentication is necessary for exploitation. Technical details are known, and a public exploit has been developed by Alessandro Magnosi and released to the public.

## Proof-of-Concept

To reproduce the vulnerability the below steps should be followed: 

* Install the service on a web server
* Uninstall and delete (if present) the Facebook auth plugin
* Upload and install the crafted Facebook Auth PoC plugin
* Apply changes restarting the application
* Navigate to the path: /Admin/FacebookAuthentication/Configure?token=76a4bfb031f9cb97fd4a739cbc3400b65397cf34&cmd=
* Put any command to test the web shell 

For ease to use, a proof-of-concept script has been provided, that could open a reverse tcp connection between the NopCommerce server and the attacker machine, giving to the attacker shell access to the server.
Note that the vulnerability has been tested thoroughly on different IIS versions and on the docker appliance. In some cases, the antivirus would get rid of one executable contained in the crafted plugin; in these cases, the attacker would still have web shell access, but obtaining interactive shell access would require additional effort.

For further information, please see the proof of concept script.

## Remediation

As the plugin system allows developers to implement their plugins by design, there is no fix that could solve this issue. There is no intention to implement an application level mitigation. It is hence strongly recommended to run the hosting server with the least level of privilege possible, and to keep the underling OS up-to-date, in order to mitigate the risk of server takeover. 

## References

*  https://www.owasp.org/index.php/Unrestricted_File_Upload
*  https://www.acunetix.com/websitesecurity/introduction-web-shells/
*  https://codedharma.com/posts/dotnet-core-webshell/

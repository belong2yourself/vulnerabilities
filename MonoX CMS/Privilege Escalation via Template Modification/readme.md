# Privilege Escalation via Template Modification

## Summary

The application allows admin to modify ASPX templates for the entire site. This behaviour could be exploited to achieve a Privilege Escalation (from web application access to OS-shell access). This can be easily done by modifying a template with a known ASPX WebShell, which will allow to execute arbitrary commands to.

Affected is the file `MonoX.MonoSoftware.MonoX.Admin.PageManagerPageTemplates`, as it allows to upload an arbitrary ASPX template via the `ctlUpload_radUploadfile0` parameter. The manipulation of a page template leads to remote command execution on the underlying server. CWE is classifying the issue as CWE-553. This is going to have an impact on confidentiality, integrity, and availability.

The weakness was discovered during April 2020 and it is uniquely identified as CVE-2020-XXXX. The exploitability is told to be trivial. It is possible to launch the attack remotely. A single authentication is necessary for exploitation. Technical details are known, but no public exploit has been released to the public.

## Proof-of-Concept

To reproduce the vulnerability the below steps should be followed: 

* Install the service on a web server
* Login to the server as admin
* Navigate to Admin Area->Pages 
* Right Click to a page (e.g. Blog.aspx)
* From the drop-down menu, choose manage templates
* Upload the PoC template (i.e template.aspx), choose it as the template for the page and save
* Navigate to http://monox.local/Blog.aspx
* See the webshell

## Remediation

No official fix is available for this issue.

## References

*  https://www.owasp.org/index.php/Unrestricted_File_Upload
*  https://www.acunetix.com/websitesecurity/introduction-web-shells/
*  https://codedharma.com/posts/dotnet-core-webshell/

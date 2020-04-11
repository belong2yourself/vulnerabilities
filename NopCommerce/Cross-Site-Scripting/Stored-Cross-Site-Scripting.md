# Admin Area - Stored Cross-Site-Scripting

## Summary

The application does not consistently validate client side input, and as a result of this it was identified that the web application was vulnerable to Stored Cross-Site Scripting.

The affected functionality is the SaveStoreMappings of the components \Presentation\Nop.Web\Areas\Admin\Controllers\NewsController.cs and \Presentation\Nop.Web\Areas\Admin\Controllers\BlogController.cs. CWE classifies this vulnerability as CWE-79. The issue is know to affect confidentiality and integrity. The issue is handled as CVE ID yet.

The issue was discovered by Alessandro Magnosi (d3adc0de) on 12/04/2019 and was named CVE-2019-19682 since 12/09/2019. The exploitability is told to be easy. It is possible to launch the attack remotely. A single authentication is necessary for exploitation. Technical details are known as well as a proof-of-concept payload, but no real exploit has been released. 

There is no information about possible countermeasures known. It may be suggested to replace the affected object with an alternative product.

It should be noted that the vulnerability has been found within an HTML content editor, which is naturally more affected by this kind of vulnerability, as the user can directly control the HTML structure of the page. The vendor reported the issue to be a “feature”. However, it was possible to note that a great effort had been made in order to avoid Cross-Site-Scripting, so it was chosen to classify that as an issue. 
 
## Proof-of-Concept

**Sample affected URL:**

* http://[Hostname]/Admin/News/NewsItemEdit/[id]
* http://[Hostname]/Admin/Blog/BlogPostEdit/[id]

**Sample affected parameter:**

```
Body
Full
```

Please note that the above might not be an exhaustive list, and that any point where an HTML Editor is used through the application may be vulnerable as well.

To reproduce the issue, the following steps can be used:

* Install the service on a web server
* Navigate through the PoC URLs
* On “Full Description” area, click on “Tools->Source Code”
* Wherever within the code, insert the following:
```<audio src="" onloadstart="alert('Stored-XSS')"></audio>```
* Save and click on Preview
* An alert box will appear on the screen


## Remediation

The developer categorised this issue as to be "by design", even if the html editor forbids the use of common XSS vectors (such as script, iframe, object tags, event handlers as "onxxx", ..., etc). There is no official plan to fix this issue in the future time. However, considering the restriction in place, a fix is expected to be applied in next versions.  

## References

* https://www.owasp.org/index.php/Cross-site_Scripting_(XSS) 
* https://www.google.com/intl/en/about/appsecurity/learning/xss/ 
* https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet 

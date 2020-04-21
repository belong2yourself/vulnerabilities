# Remote Code Execution via Insecure Deserialization

## Summary

A vulnerability has been found in the MonoX CMS for .NET up to v5.1.40.5152, which allows remote code execution via insecure deserialization. During the review, it was possible to see that the application used serialization to transfer objects over the network. In certain cases, this process could be exploited by an attacker, which could deserialize arbitrary objects, leading to remote code execution. Multiple classes were found to be affected by this issue, such as:

* `MonoX.MonoSoftware.MonoX.ModuleGallery.HTML5Upload`
* `MonoX.MonoSoftware.MonoX.ModuleGallery.SilverLightUploadModule`
* `MonoX.MonoSoftware.MonoX.HTML5Upload` 
* `MonoX.MonoSoftware.MonoX.SilverLightUploadHandler`

The exploitable URLs were found to be:

* `/MonoX/Pages/SocialNetworking/lng/en-US/PhotoGallery.aspx`
* `/MonoX/HTML5Upload.ashx`

All the instances showed to be exploitable, leading to arbitrary code execution.

* [PhotoGallery](https://github.com/belong2yourself/vulnerabilities/tree/master/MonoX%20CMS/Remote%20Code%20Execution%20via%20Insecure%20Deserialization/Actions%20-%20Authenticated%20PHP%20Object%20Injection)
* [HTML5Upload](https://github.com/belong2yourself/vulnerabilities/tree/master/MonoX%20CMS/Remote%20Code%20Execution%20via%20Insecure%20Deserialization/Subpages%20-%20Authenticated%20PHP%20Object%20Injection)

For further information, please refer to the single vulnerabilities.

## Remediation

Currently, no fixes are available for the issues.

## References

*   [https://cwe.mitre.org/data/definitions/1236.html](https://cwe.mitre.org/data/definitions/1236.html)
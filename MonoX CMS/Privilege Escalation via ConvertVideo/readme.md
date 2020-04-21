# Privilege Escalation via ConvertVideo

## Summary

The application allows to host videos and audio files within news and blog posts, converting them on the fly in regular flash videos. The conversion is handled internally calling a conversion executable (ffmpeg.exe). The settings panel allows admin to set the location of ffmpeg executable within the server, to accomodate different installations. However, if an attacker had the capability to modify the Coverter Executable Path, this behaviour could be exploited to achieve a Privilege Escalation (from web application access to OS-shell access). This can be easily done uploading an executable, changing the Converter Exe Path to point to the uploaded executable, than upload a video to a blog post.

Affected are the files `MonoX.MonoSoftware.MonoX.Video.FlvEncoder` and `MonoX.MonoSoftware.MonoX.Video.Mp4Encoder`, as they do not check the validity of `ffmpeg.exe` file before executing it. The manipulation of the `ffmpeg.exe` executable leads to remote command execution on the underlying server. CWE is classifying the issue as CWE-269. This is going to have an impact on confidentiality, integrity, and availability.

The weakness was discovered during April 2020 and it is uniquely identified as CVE-2020-XXXX. The exploitability is told to be trivial. It is possible to launch the attack remotely. A single authentication is necessary for exploitation. Technical details are known, but no public exploit has been released to the public.

## Proof-of-Concept

To reproduce the vulnerability the below steps should be followed: 

* Install the service on a web server
* Login to the server as admin
* From Admin Panel->Site Settings, modify the Video Converter Exe Path to `C:\Windows\System32\calc.exe`
* Navigate to create blog post
* Upload a video
* From the task manager, see that a calculator process is spawn within the system

## Remediation

No official fix is available for this issue.

## References

*  https://www.owasp.org/index.php/Unrestricted_File_Upload
*  https://www.acunetix.com/websitesecurity/introduction-web-shells/
*  https://codedharma.com/posts/dotnet-core-webshell/

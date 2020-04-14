# Arbitrary File Deletion via Insecure Deserialization

## Summary

A vulnerability has been found in the Subrion CMS up to v4.2.2, which allows code execution via insecure deserialization. During the review, it was found that the application heavily uses serialization to store and load object from and to the database. In certain cases, this process could be manipulated by an attacker, which could deserialize arbitrary objects, leading to code execution. Multiple files were found to be affected by this issue, such as:

* `/front/actions.php`
* `/admin/blocks.php`
* `/includes/classes/ia.core.users.php` 

In particular, the first two instances showed to be exploitable, leading to arbitrary file deletion.

* ~~[Actions](https://github.com/belong2yourself/vulnerabilities/tree/master/Subrion%20CMS/Insecure%20Deserialization/Actions%20-%20Authenticated%20PHP%20Object%20Injection)~~ Fixed in Latest Branch
* [Subpages](https://github.com/belong2yourself/vulnerabilities/tree/master/Subrion%20CMS/Insecure%20Deserialization/Subpages%20-%20Authenticated%20PHP%20Object%20Injection)

**Note:** The vulnerability affecting `/front/actions.php`, is the result of a parallel research by MS509 and myself. However, as they firstly notified the issue to Intelliants, kudos to them!

For further information, please refer to the single vulnerabilities.

## Remediation

Currently, no fixes are available for this issue.

## References

*   [https://cwe.mitre.org/data/definitions/1236.html](https://cwe.mitre.org/data/definitions/1236.html)
*   [https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection](https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection)
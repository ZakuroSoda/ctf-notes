# Misc

## Zipslips

Refer to this: https://security.snyk.io/research/zip-slip-vulnerability

> Zip Slip is a form of directory traversal that can be exploited by extracting files from an archive. The premise of the directory traversal vulnerability is that an attacker can gain access to parts of the file system outside of the target folder in which they should reside. The attacker can then overwrite executable files and either invoke them remotely or wait for the system or user to call them, thus achieving remote command execution on the victim’s machine. The vulnerability can also cause damage by overwriting configuration files or other sensitive resources, and can be exploited on both client (user) machines and servers.

```
┌──(kali㉿kali)-[~]
└─$ ln -s ../../../../../../flag.txt symlink

┌──(kali㉿kali)-[~]
└─$ zip --symlinks exploit.zip symlink
  adding: test3 (stored 0%)
```

If the application returns the files to you, then you can read files which you know exist!
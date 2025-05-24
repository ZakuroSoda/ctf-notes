# Misc

## Forensics - Writing RTP Streams from Captures to .mp4 Video

Note that you do NOT need tshark for this.

1. Open the capture file in Wireshark.
2. In the top menu, go to `Telephony` > `RTP` > `RTP Streams`.
3. Select the RTP stream you want to export.
4. At the bottom, click on Export. The stream will be exported as a .rtpdump file.
5. Now, you need to install `ffmpeg` (`sudo apt install ffmpeg`) and `rtptools` from https://github.com/irtlab/rtptools.
6. Once done, we will play the stream using `rtpplay` and pipe it to `ffmpeg` to convert it to a .mp4 file.
   1. In one terminal, run: `rtpplay -T -f <path_to_rtpdump_file> 127.0.0.1/5004`
   2. In another terminal, create a sdp file as shown below.
   3. In this terminal, run: `ffmpeg -protocol_whitelist file,udp,rtp -i stream.sdp -c copy output.mp4`
   4. If you face any problems, try running ffmpeg FIRST before rtpplay.
  
SDP File:
```
v=0
o=- 0 0 IN IP4 127.0.0.1
s=No Name
c=IN IP4 127.0.0.1
t=0 0
m=video 5004 RTP/AVP 96
a=rtpmap:96 H264/90000
```


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
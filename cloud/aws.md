# AWS

Amazon web services is a cloud service provider.  
In particular, they offer something called `S3 buckets`, which is basically something similar to a google drive folder.  

One popular use case is hosting static sites.  
> When hosting a site as an S3 bucket, the bucket name (flaws.cloud) must match the domain name (flaws.cloud). Also, S3 buckets are a global name space, meaning two people cannot have buckets with the same name. The result of this is you could create a bucket named apple.com and Apple would never be able host their main site via S3 hosting.

For this use case:
1. Upload your files using GUI, CLI or FileZilla etc
2. Enable Static Website Hosting
3. Allow public access
4. Configure DNS

```DNS
www.example.com.  IN CNAME  example-bucket.s3-website-us-west-2.amazonaws.com.
```

All S3 buckets, when configured for web hosting, are given an AWS domain you can use to browse to it without setting up your own DNS.  

With the domain, the first step is to `dig` and `nslookup`.  

```bash
┌──(kali㉿kali)-[~]
└─$ dig flaws.cloud    
...
;; ANSWER SECTION:
flaws.cloud.            5       IN      A       52.92.163.115
flaws.cloud.            5       IN      A       52.92.177.107
flaws.cloud.            5       IN      A       52.92.160.51
flaws.cloud.            5       IN      A       52.92.147.19
flaws.cloud.            5       IN      A       52.92.241.19
flaws.cloud.            5       IN      A       52.92.149.115
flaws.cloud.            5       IN      A       52.218.205.90
flaws.cloud.            5       IN      A       52.218.240.187
...

//if you visit one of the IPs, it should redirect you to amazon s3.

┌──(kali㉿kali)-[~]
└─$ nslookup 52.92.163.115
115.163.92.52.in-addr.arpa      name = s3-website-us-west-2.amazonaws.com
```

By the way, now we know the mirror link to be
http://flaws.cloud.s3-website-us-west-2.amazonaws.com/  

This is because of aws reserved domain thing.  

If the permissions are lose to explore the bucket, we can do  
```bash
aws s3 ls  s3://flaws.cloud/ --no-sign-request --region us-west-2
```
or  
https://cyberduck.io/  
or  
http://flaws.cloud.s3.amazonaws.com/
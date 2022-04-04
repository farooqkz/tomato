# API of Tomato

### GET `/dot.png`

Increase hit count for the referer page by one.

### GET `/whoami`

Returns

```json
{ "youre": "noone | admin" }
```

### GET `/stats`

Returns an object which for each entry, the key is the URL and the total hit of the URL.

Example:

```json
{
  "http://far.chickenkiller.com/": 1000
}
```


There is also a special `total` entry showing the sum from all pages.


### GET `/useragent/<text>`

greps between useragent strings for `<text>`. Resulting in a JSON with count of found and count of total:

```json
{
  "result": 3,
  "total": 5
}
```

### GET `/login`

Get the login method.

```json
{ "method": "open|auth" }
```

`auth` means this instance requires authentication to access statistics data.

And `open` means anyone can access the statistics data.

### POST `/login`

Log in for the admin:

```json
{
  "username": "farooqkz",
  "password": "a password which I dont even tell my mom about it",
}
```

Response is:

```json
{ "logged_in": "success|fail" }
```

If login method for the server has been configured as `open`, this endpoint always returns `success` and changes the session data accordingly.

### GET `/logout`

Log out for the admin. Returns nothing

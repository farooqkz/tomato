# API of Tomato

### GET `/dot.png`

Increase hit count for the referrer page by one.

### GET `/whoami`

Returns

```json
{ "youre": "noone | admin" }
```

### GET `/stats`

Returns an object which for each entry, the key is the URL and the value
is a Stats object.

Stats object is an object like this:

```json
{
  "total": 1400,
  "24h": 400,
  "1w": 500,
  "1m": 900
}
```

### GET `/browsers`

To be documented.

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

### GET `/logout`

Log out for the admin. Returns nothing

# pytest-loco-http

HTTP support for `pytest-loco`.

The `pytest-loco-http` extension provides first-class HTTP support for the
`pytest-loco` DSL. It introduces a set of HTTP actors (`http.get`,
`http.post`, `http.put`, `http.delete`, etc.) that execute real HTTP
requests using managed sessions and return normalized, structured
response objects.

## Install

```sh
> pip install pytest-loco-http
```

Requirements:
- Python 3.13 or higher

## Requests

Each HTTP method is exposed as an actor:

- `http.get`
- `http.post`
- `http.put`
- `http.patch`
- `http.delete`
- `http.head`
- `http.options`

Every actor accepts a common set of parameters and produces a normalized
response object in the execution context.

For example:

```yaml
title: Simple GET request
action: http.get
url: https://httpbin.org/get
timeout: 30
expect:
  - title: Status is 200
    value: !var result.status
    match: 200
```

Sessions are managed automatically. You may optionally specify a
logical `session` name (`default` by default).

## Responses

Response fields include:
- `status` - HTTP status
- `headers` - normalized response headers (lowercase keys)
- `cookies` - list of structured cookies
- `body` - raw response body (bytes)
- `text` - response body as text
- `request` - structured original request
- `history` - redirect chain (list of responses)

For example:

```yaml
...
expect:
  - title: Response contains expected text
    value: !var result.text
    regexMatch: httpbin\.org
    multiline: yes
```

Redirect history can be inspected:

```yaml
...
export:
  firstRedirect: !var result.history.0
```

## Query parameters

Query parameters can be passed using the `params` field (aliases: `query`, `queryParams`).

```yaml
action: http.get
url: https://httpbin.org/get
params:
  test: "true"
expect:
  - title: Query is echoed
    value: !var result.text
    regex: \?test=true
    multiline: yes
```

Query parameters are automatically encoded and appended to the URL.

## Data

The `data` field allows sending raw request bodies as `str` or `bytes`.

```yaml
---
action: http.post
url: https://httpbin.org/post
data: |
  {"message": "hello"}
headers:
  content-type: application/json
expect:
  - title: Status is 200
    value: !var result.status
    match: 200
```

The raw body is preserved in the response model as:
- `request.body` as bytes
- `request.text` as text

## Files

Multipart file uploads are supported via the files field.

Each file entry defines:
- `name` — form field name
- `content` — string or bytes
- `filename` (optional)
- `mimetype` (optional)

If `mimetype` is not provided, it is inferred:
- `application/octet-stream` for bytes
- `text/plain` for strings

### Binary file

```yaml
action: http.post
url: https://httpbin.org/post
files:
  - name: test
    content: !binaryHex |
      48 65 6C 6C 6F 2C 20
      57 6F 72 6C 64 21
expect:
  - title: Status is 200
    value: !var result.status
    match: 200
```

### Text file

```yaml
action: http.post
url: https://httpbin.org/post
files:
  - name: test
    content: Hello, World!
expect:
  - title: File content is echoed
    value: !var result.text
    regex: '"Hello, World!"'
    multiline: yes
```

## Instructions

Provide `!urljoin` instruction that compose a URL at runtime by joining
a base URL from the DSL context with a postfix path.

This instruction is useful when endpoints depend on previously resolved
values (e.g. environment-specific base URLs, dynamically returned URLs,
or configuration variables).

Syntax:

```
!urljoin <variable> <postfix>
```

- `<variable>` — name of a context variable containing a base URL;
- `<postfix>` — relative path segment to append to the base URL.

Both parts must be separated by whitespace.

For example:

```yaml
...
vars:
  baseUrl: https://api.example.com
action: http.get
url: !urljoin baseUrl api/v1/users
...
```

Resulting URL at runtime: `https://api.example.com/api/v1/users`

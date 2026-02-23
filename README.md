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

## Documentation

See https://pytest-loco.readthedocs.io/en/latest/extensions/http/index.html

## Thanks

- [Requests](https://requests.readthedocs.io/en/latest/)

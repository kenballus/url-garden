import sys
import os
import base64
import rfc3986
import afl

afl.init()

parsed_url = rfc3986.ParseResult.from_string(
    sys.stdin.buffer.read(), encoding="latin1", strict=True, lazy_normalize=False
)

result: dict[str, str] = {}
result["scheme"] = parsed_url.scheme
result["userinfo"] = parsed_url.userinfo
result["host"] = parsed_url.host
result["port"] = str(parsed_url.port) if parsed_url.port is not None else ""
result["path"] = parsed_url.path
result["query"] = parsed_url.query
result["fragment"] = parsed_url.fragment

for k, v in result.items():
    if v is None:
        v = ""
    result[k] = base64.b64encode(v.encode("latin1")).decode("latin1")

print(
    "{"
    + ",".join(
        f"\"{k}\":\"{result[k]}\""
        for k, v in result.items()
    )
    + "}",
    flush=True,
)

os._exit(0)

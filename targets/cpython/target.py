import sys
import os
import base64
import urllib.parse
import afl

afl.init()

parsed_url = urllib.parse.urlparse(sys.stdin.buffer.read())

result: dict[str, str] = {}
result["scheme"] = parsed_url.scheme.decode("latin1")
result["userinfo"] = (parsed_url.username or b"").decode("latin1") + (":" + parsed_url.password.decode("latin1") if parsed_url.password is not None else "")
result["host"] = (parsed_url.hostname or b"").decode("latin1")
result["port"] = str(parsed_url.port) if parsed_url.port is not None else ""
result["path"] = parsed_url.path.decode("latin1")
result["query"] = parsed_url.query.decode("latin1")
result["fragment"] = parsed_url.fragment.decode("latin1")

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

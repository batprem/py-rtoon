import orjson
from py_rtoon import encode_default, decode_default

data = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
}

toon = encode_default(orjson.dumps(data).decode())
print(toon)

decoded = decode_default(toon)
print(decoded)

assert data == orjson.loads(decoded)

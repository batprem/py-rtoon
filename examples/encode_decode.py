from py_rtoon import encode_default, decode_default

data = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
}

toon = encode_default(data)
print(toon)

decoded = decode_default(toon)
print(decoded)

assert data == decoded

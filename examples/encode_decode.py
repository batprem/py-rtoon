from py_rtoon import encode_default, decode_default

data = {
    "tags": ["jazz", "chill", "lofi"],
    "user": "John Doe"
}

toon = encode_default(data)
print(toon)

# Output:
# tags[3]: jazz,chill,lofi
# user: John Doe

decoded = decode_default(toon)
print(decoded)

# Output:
# {'tags': ['jazz', 'chill', 'lofi'], 'user': 'John Doe'}
assert data == decoded

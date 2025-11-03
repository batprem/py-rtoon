"""Python bindings for rtoon - Token-Oriented Object Notation."""

import orjson
from py_rtoon._core import (
    hello_from_bin,
    encode_default as _encode_default_str,
    decode_default as _decode_default_str,
    encode as _encode_str,
    decode as _decode_str,
    Delimiter,
    EncodeOptions,
    DecodeOptions,
)

__all__ = [
    "hello_from_bin",
    "encode_default",
    "decode_default",
    "encode",
    "decode",
    "Delimiter",
    "EncodeOptions",
    "DecodeOptions",
    "hello",
]


def hello() -> str:
    """Example function that demonstrates rtoon encoding.

    Returns:
        A TOON-formatted string with example data
    """
    return hello_from_bin()


def encode_default(data: dict | list | str) -> str:
    """Encode data to TOON format using default options.

    Accepts Python dict, list, or JSON string and encodes to TOON format.

    Args:
        data: Python dict, list, or JSON string to encode

    Returns:
        A TOON-formatted string

    Raises:
        ValueError: If the data is invalid or encoding fails
        TypeError: If data type is not supported

    Examples:
        >>> import py_rtoon
        >>> # Encode dict directly
        >>> data = {"name": "Alice", "age": 30}
        >>> toon = py_rtoon.encode_default(data)
        >>> print(toon)
        age: 30
        name: Alice

        >>> # Encode list directly
        >>> data = [1, 2, 3]
        >>> toon = py_rtoon.encode_default(data)
        >>> print(toon)
        [3]: 1,2,3

        >>> # Encode JSON string
        >>> import json
        >>> toon = py_rtoon.encode_default(json.dumps(data))
    """
    if isinstance(data, str):
        # Already a JSON string
        return _encode_default_str(data)
    elif isinstance(data, (dict, list)):
        # Convert to JSON string
        json_str = orjson.dumps(data).decode()
        return _encode_default_str(json_str)

    raise TypeError(
        f"Data must be dict, list, or JSON string, got {type(data).__name__}"
    )


def decode_default(toon_str: str) -> dict:
    """Decode a TOON string to Python dict or JSON string.

    Args:
        toon_str: A TOON-formatted string to decode

    Returns:
        Python dict

    Raises:
        ValueError: If the TOON string is invalid or decoding fails

    Examples:
        >>> import py_rtoon
        >>> toon = "name: Alice\\nage: 30"
        >>> # Decode to dict (default)
        >>> data = py_rtoon.decode_default(toon)
        >>> print(data)
        {'name': 'Alice', 'age': 30}

        >>> # Decode to JSON string
        >>> data = py_rtoon.decode_default(toon)
        >>> print(data)
        {'name': 'Alice', 'age': 30}
    """
    return orjson.loads(_decode_default_str(toon_str))


def encode(data: dict | list | str, options: EncodeOptions) -> str:
    """Encode data to TOON format with custom options.

    Args:
        data: Python dict, list, or JSON string to encode
        options: EncodeOptions for customizing the output format

    Returns:
        A TOON-formatted string

    Raises:
        ValueError: If the data is invalid or encoding fails
        TypeError: If data type is not supported

    Examples:
        >>> import py_rtoon
        >>> data = {"tags": ["a", "b", "c"]}
        >>> options = py_rtoon.EncodeOptions().with_delimiter(py_rtoon.Delimiter.pipe())
        >>> toon = py_rtoon.encode(data, options)
        >>> print(toon)
        tags[3|]: a|b|c
    """
    if isinstance(data, str):
        return _encode_str(data, options)
    elif isinstance(data, (dict, list)):
        json_str = orjson.dumps(data).decode()
        return _encode_str(json_str, options)
    else:
        raise TypeError(
            f"Data must be dict, list, or JSON string, got {type(data).__name__}"
        )


def decode(toon_str: str, options: DecodeOptions) -> dict:
    """Decode a TOON string to Python dict or JSON string with custom options.

    Args:
        toon_str: A TOON-formatted string to decode
        options: DecodeOptions for customizing the decoding behavior

    Returns:
        Python dict

    Raises:
        ValueError: If the TOON string is invalid or decoding fails

    Examples:
        >>> import py_rtoon
        >>> toon = "items[2]: a,b"
        >>> options = py_rtoon.DecodeOptions().with_strict(False)
        >>> data = py_rtoon.decode(toon, options)
        >>> print(data)
        {'items': ['a', 'b']}
    """
    return orjson.loads(_decode_str(toon_str, options))

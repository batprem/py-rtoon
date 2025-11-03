"""Python bindings for rtoon - Token-Oriented Object Notation."""

from py_rtoon._core import (
    hello_from_bin,
    encode_default,
    decode_default,
    encode,
    decode,
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

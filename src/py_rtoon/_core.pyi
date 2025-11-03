"""Type stubs for _core module (Rust extension)."""

def hello_from_bin() -> str:
    """Example function that demonstrates rtoon encoding.

    Returns:
        A TOON-formatted string with example data
    """
    ...

def encode_default(json_str: str) -> str:
    """Encode a JSON string to TOON format using default options.

    Args:
        json_str: A JSON string to encode

    Returns:
        A TOON-formatted string

    Raises:
        ValueError: If the JSON is invalid or encoding fails
    """
    ...

def decode_default(toon_str: str) -> str:
    """Decode a TOON string to JSON format using default options.

    Args:
        toon_str: A TOON-formatted string to decode

    Returns:
        A JSON string

    Raises:
        ValueError: If the TOON string is invalid or decoding fails
    """
    ...

def encode(json_str: str, options: EncodeOptions) -> str:
    """Encode a JSON string to TOON format with custom options.

    Args:
        json_str: A JSON string to encode
        options: EncodeOptions for customizing the output format

    Returns:
        A TOON-formatted string

    Raises:
        ValueError: If the JSON is invalid or encoding fails
    """
    ...

def decode(toon_str: str, options: DecodeOptions) -> str:
    """Decode a TOON string to JSON format with custom options.

    Args:
        toon_str: A TOON-formatted string to decode
        options: DecodeOptions for customizing the decoding behavior

    Returns:
        A JSON string

    Raises:
        ValueError: If the TOON string is invalid or decoding fails
    """
    ...

class Delimiter:
    """Delimiter options for encoding TOON format."""

    @staticmethod
    def comma() -> Delimiter:
        """Comma delimiter (default)."""
        ...

    @staticmethod
    def pipe() -> Delimiter:
        """Pipe delimiter."""
        ...

    @staticmethod
    def tab() -> Delimiter:
        """Tab delimiter."""
        ...

class EncodeOptions:
    """Options for encoding to TOON format."""

    def __init__(self) -> None:
        """Create new encoding options with defaults."""
        ...

    def with_delimiter(self, delimiter: Delimiter) -> EncodeOptions:
        """Set the delimiter for arrays and inline objects.

        Args:
            delimiter: The delimiter to use

        Returns:
            A new EncodeOptions instance with the delimiter set
        """
        ...

    def with_length_marker(self, marker: str) -> EncodeOptions:
        """Set the length marker character for arrays.

        Args:
            marker: A single character to use as length marker

        Returns:
            A new EncodeOptions instance with the length marker set
        """
        ...

class DecodeOptions:
    """Options for decoding TOON format."""

    def __init__(self) -> None:
        """Create new decoding options with defaults."""
        ...

    def with_strict(self, strict: bool) -> DecodeOptions:
        """Enable or disable strict mode (validates array lengths).

        Args:
            strict: Whether to enable strict mode

        Returns:
            A new DecodeOptions instance with strict mode set
        """
        ...

    def with_coerce_types(self, coerce: bool) -> DecodeOptions:
        """Enable or disable type coercion.

        Args:
            coerce: Whether to enable type coercion

        Returns:
            A new DecodeOptions instance with type coercion set
        """
        ...

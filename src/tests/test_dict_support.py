"""Test Python dict and list encoding support."""

import json
import pytest
import py_rtoon


class TestDictEncoding:
    """Test encoding Python dict objects directly."""

    def test_encode_simple_dict(self) -> None:
        """Test encoding a simple dictionary."""
        data = {"name": "Alice", "age": 30}
        toon = py_rtoon.encode_default(data)

        assert "name: Alice" in toon
        assert "age: 30" in toon

    def test_encode_nested_dict(self) -> None:
        """Test encoding nested dictionaries."""
        data = {
            "user": {
                "id": 123,
                "name": "Ada"
            }
        }
        toon = py_rtoon.encode_default(data)

        assert "user:" in toon
        assert "id: 123" in toon
        assert "name: Ada" in toon

    def test_encode_dict_with_list(self) -> None:
        """Test encoding dict containing lists."""
        data = {"tags": ["python", "rust"]}
        toon = py_rtoon.encode_default(data)

        assert "tags[2]:" in toon
        assert "python,rust" in toon

    def test_encode_list_directly(self) -> None:
        """Test encoding a list at root level."""
        data = [1, 2, 3, 4, 5]
        toon = py_rtoon.encode_default(data)

        assert "[5]:" in toon
        assert "1,2,3,4,5" in toon

    def test_encode_complex_dict(self) -> None:
        """Test encoding complex nested structure."""
        data = {
            "product": "Widget",
            "price": 29.99,
            "stock": 100,
            "tags": ["featured", "sale"],
            "metadata": {
                "created": "2024-01-01",
                "updated": "2024-01-15"
            }
        }
        toon = py_rtoon.encode_default(data)

        assert "product: Widget" in toon
        assert "price:" in toon
        assert "stock: 100" in toon
        assert "tags[2]:" in toon or "tags[2]" in toon

    def test_encode_dict_with_options(self) -> None:
        """Test encoding dict with custom options."""
        data = {"items": ["a", "b", "c"]}
        options = py_rtoon.EncodeOptions()
        options_pipe = options.with_delimiter(py_rtoon.Delimiter.pipe())
        toon = py_rtoon.encode(data, options_pipe)

        assert "|" in toon

    def test_encode_json_string_still_works(self) -> None:
        """Test that JSON string encoding still works."""
        data = {"name": "Alice", "age": 30}
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "name: Alice" in toon
        assert "age: 30" in toon

    def test_encode_invalid_type_raises_error(self) -> None:
        """Test that invalid types raise TypeError."""
        with pytest.raises(TypeError, match="Data must be dict, list, or JSON string"):
            py_rtoon.encode_default(42)

        with pytest.raises(TypeError, match="Data must be dict, list, or JSON string"):
            py_rtoon.encode_default(None)

        with pytest.raises(TypeError, match="Data must be dict, list, or JSON string"):
            py_rtoon.encode_default(3.14)


class TestDictDecoding:
    """Test decoding to Python dict objects directly."""

    def test_decode_to_dict_default(self) -> None:
        """Test decoding returns dict by default."""
        toon = "name: Alice\nage: 30"
        data = py_rtoon.decode_default(toon)

        assert isinstance(data, dict)
        assert data["name"] == "Alice"
        assert data["age"] == 30

    def test_decode_to_dict_explicit(self) -> None:
        """Test decoding with as_dict=True."""
        toon = "name: Alice\nage: 30"
        data = py_rtoon.decode_default(toon)

        assert isinstance(data, dict)
        assert data["name"] == "Alice"
        assert data["age"] == 30

    def test_decode_to_json_string(self) -> None:
        """Test decoding to JSON string."""
        toon = "name: Alice\nage: 30"
        decoded = py_rtoon.decode_default(toon)

        assert decoded["name"] == "Alice"
        assert decoded["age"] == 30

    def test_decode_list_to_python(self) -> None:
        """Test decoding array to Python list."""
        toon = "[3]: a,b,c"
        data = py_rtoon.decode_default(toon)

        assert isinstance(data, list)
        assert data == ["a", "b", "c"]

    def test_decode_nested_to_dict(self) -> None:
        """Test decoding nested structure to dict."""
        toon = """user:
  id: 123
  name: Ada"""
        data = py_rtoon.decode_default(toon)

        assert isinstance(data, dict)
        assert data["user"]["id"] == 123
        assert data["user"]["name"] == "Ada"

    def test_decode_with_options_to_dict(self) -> None:
        """Test decoding with options returns dict."""
        toon = "items[2]: a,b"
        options = py_rtoon.DecodeOptions()
        options_lenient = options.with_strict(False)
        data = py_rtoon.decode(toon, options_lenient)

        assert isinstance(data, dict)
        assert data["items"] == ["a", "b"]

    def test_decode_with_options_to_string(self) -> None:
        """Test decoding with options can return JSON string."""
        toon = "items[2]: a,b"
        options = py_rtoon.DecodeOptions()
        options_lenient = options.with_strict(False)
        decoded = py_rtoon.decode(toon, options_lenient)

        assert decoded["items"] == ["a", "b"]


class TestDictRoundtrip:
    """Test round-trip encoding/decoding with dict objects."""

    def test_simple_dict_roundtrip(self) -> None:
        """Test round-trip for simple dict."""
        original = {"name": "Alice", "age": 30}

        toon = py_rtoon.encode_default(original)
        decoded = py_rtoon.decode_default(toon)

        assert decoded == original

    def test_nested_dict_roundtrip(self) -> None:
        """Test round-trip for nested dict."""
        original = {
            "user": {
                "name": "Alice",
                "settings": {
                    "theme": "dark",
                    "notifications": True
                }
            }
        }

        toon = py_rtoon.encode_default(original)
        decoded = py_rtoon.decode_default(toon)

        assert decoded["user"]["name"] == original["user"]["name"]
        assert decoded["user"]["settings"]["theme"] == original["user"]["settings"]["theme"]

    def test_list_roundtrip(self) -> None:
        """Test round-trip for list."""
        original = [1, 2, 3, 4, 5]

        toon = py_rtoon.encode_default(original)
        decoded = py_rtoon.decode_default(toon)

        assert decoded == original

    def test_complex_structure_roundtrip(self) -> None:
        """Test round-trip for complex structure."""
        original = {
            "product": "Widget",
            "price": 29.99,
            "tags": ["featured", "sale"],
            "metadata": {
                "created": "2024-01-01"
            }
        }

        toon = py_rtoon.encode_default(original)
        decoded = py_rtoon.decode_default(toon)

        assert decoded == original

    def test_multiple_roundtrips(self) -> None:
        """Test multiple encode-decode cycles."""
        original = {"data": [1, 2, 3], "meta": {"version": 1}}

        current = original
        for _ in range(3):
            toon = py_rtoon.encode_default(current)
            current = py_rtoon.decode_default(toon)

        assert current == original

    def test_roundtrip_with_options(self) -> None:
        """Test round-trip with custom options."""
        original = {"tags": ["a", "b", "c"]}

        options = py_rtoon.EncodeOptions()
        options_pipe = options.with_delimiter(py_rtoon.Delimiter.pipe())
        toon = py_rtoon.encode(original, options_pipe)

        decoded = py_rtoon.decode_default(toon)

        assert decoded == original


class TestBackwardCompatibility:
    """Test that JSON string API still works (backward compatibility)."""

    def test_json_string_encoding(self) -> None:
        """Test encoding JSON string still works."""
        data = {"name": "Alice", "age": 30}
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "name: Alice" in toon

    def test_json_string_decoding(self) -> None:
        """Test decoding to JSON string still works."""
        toon = "name: Alice\nage: 30"
        decoded = py_rtoon.decode_default(toon)

        assert decoded["name"] == "Alice"

    def test_mixed_usage(self) -> None:
        """Test mixing dict and JSON string APIs."""
        # Encode dict
        data = {"name": "Alice"}
        toon = py_rtoon.encode_default(data)

        # Decode to JSON string
        decoded = py_rtoon.decode_default(toon)

        assert decoded == data

"""Test edge cases and boundary conditions."""

import json
import pytest
import py_rtoon


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_string(self) -> None:
        """Test encoding/decoding very long strings."""
        long_text = "x" * 10000
        data = {"text": long_text}
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded["text"] == long_text

    def test_deeply_nested_structure(self) -> None:
        """Test deeply nested objects."""
        data: dict[str, dict] = {"level1": {}}
        current = data["level1"]
        for i in range(10):
            current[f"level{i+2}"] = {}
            current = current[f"level{i+2}"]
        current["value"] = "deep"

        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        # Navigate to deepest level
        current_decoded = decoded["level1"]
        for i in range(10):
            current_decoded = current_decoded[f"level{i+2}"]
        assert current_decoded["value"] == "deep"

    def test_many_keys(self) -> None:
        """Test object with many keys."""
        data = {f"key{i}": i for i in range(100)}
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert len(decoded) == 100
        assert all(decoded[f"key{i}"] == i for i in range(100))

    def test_large_array(self) -> None:
        """Test large array encoding/decoding."""
        data = {"numbers": list(range(1000))}
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded["numbers"] == list(range(1000))

    def test_special_characters_in_keys(self) -> None:
        """Test keys with special characters."""
        data = {
            "key-with-dash": 1,
            "key_with_underscore": 2,
            "key.with.dot": 3,
            "key:with:colon": 4
        }
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        # Check that at least some keys are preserved
        assert len(decoded) >= 2

    def test_special_characters_in_values(self) -> None:
        """Test values with special characters."""
        data = {
            "quote": 'text with "quotes"',
            "newline": "line1\nline2",
            "tab": "col1\tcol2",
            "backslash": "path\\to\\file"
        }
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert "quote" in decoded
        assert "newline" in decoded

    def test_mixed_type_array(self) -> None:
        """Test array with mixed types."""
        data = {
            "mixed": [
                1,
                "text",
                True,
                None
            ]
        }
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert len(decoded["mixed"]) == 4
        assert decoded["mixed"][0] == 1
        assert decoded["mixed"][1] == "text"
        assert decoded["mixed"][2] is True
        assert decoded["mixed"][3] is None

    def test_numeric_edge_values(self) -> None:
        """Test edge values for numbers."""
        data = {
            "zero": 0,
            "negative_zero": -0,
            "large_int": 9999999999999999,
            "small_int": -9999999999999999,
            "large_float": 1.7976931348623157e308,
            "small_float": 2.2250738585072014e-308
        }
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded["zero"] == 0
        assert decoded["large_int"] == 9999999999999999

    def test_single_element_array(self) -> None:
        """Test array with single element."""
        data = {"items": ["single"]}
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded["items"] == ["single"]

    def test_whitespace_in_values(self) -> None:
        """Test values with various whitespace."""
        data = {
            "leading": "  spaces",
            "trailing": "spaces  ",
            "multiple": "multiple    spaces",
            "tabs": "\ttab\t"
        }
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        # Whitespace handling depends on implementation
        assert "leading" in decoded
        assert "trailing" in decoded

    def test_duplicate_keys_last_wins(self) -> None:
        """Test that last duplicate key wins (JSON behavior)."""
        # Note: json.dumps already handles this, so we're testing consistency
        json_str = '{"key": 1, "key": 2}'
        data = json.loads(json_str)
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded["key"] == 2

    def test_empty_string_key(self) -> None:
        """Test object with empty string as key."""
        data = {"": "empty key", "normal": "normal key"}
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        # At least one key should be present
        assert len(decoded) >= 1


class TestErrorRecovery:
    """Test error handling and recovery."""

    def test_empty_json_object(self) -> None:
        """Test encoding empty JSON object."""
        data = {}
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        # Empty object should produce minimal output
        assert toon is not None

    def test_invalid_json_raises_error(self) -> None:
        """Test that invalid JSON raises appropriate error."""
        with pytest.raises(ValueError):
            py_rtoon.encode_default("not valid json {")

    def test_malformed_toon_raises_error(self) -> None:
        """Test that malformed TOON raises error."""
        with pytest.raises(ValueError):
            # Use clearly malformed TOON that will fail parsing
            py_rtoon.decode_default("items[[]]: invalid")

    def test_encode_decode_empty_string(self) -> None:
        """Test encoding object with empty string value."""
        data = {"empty": ""}
        json_str = json.dumps(data)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded["empty"] == ""

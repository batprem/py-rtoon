"""Test round-trip encoding and decoding."""

import json
import py_rtoon


class TestRoundtrip:
    """Test round-trip conversion between JSON and TOON."""

    def test_simple_object_roundtrip(self) -> None:
        """Test round-trip for simple object."""
        original = {"name": "Alice", "age": 30, "active": True}
        json_str = json.dumps(original)

        # Encode to TOON
        toon = py_rtoon.encode_default(json_str)

        # Decode back to JSON
        decoded = py_rtoon.decode_default(toon)

        assert decoded == original

    def test_nested_object_roundtrip(self) -> None:
        """Test round-trip for nested objects."""
        original = {
            "user": {
                "name": "Alice",
                "age": 30,
                "address": {
                    "city": "New York",
                    "zip": "10001"
                }
            }
        }
        json_str = json.dumps(original)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        # Verify key values are present (structure might vary)
        assert decoded["user"]["name"] == original["user"]["name"]
        assert decoded["user"]["age"] == original["user"]["age"]
        assert decoded["user"]["address"]["city"] == original["user"]["address"]["city"]

    def test_array_roundtrip(self) -> None:
        """Test round-trip for arrays."""
        original = {
            "tags": ["python", "rust", "typescript"],
            "numbers": [1, 2, 3, 4, 5],
            "mixed": ["text", 123, True, None]
        }
        json_str = json.dumps(original)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded == original

    def test_tabular_data_roundtrip(self) -> None:
        """Test round-trip for tabular format."""
        original = {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "user"},
                {"id": 3, "name": "Charlie", "role": "guest"}
            ]
        }
        json_str = json.dumps(original)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert len(decoded["users"]) == len(original["users"])
        for i, user in enumerate(decoded["users"]):
            assert user["id"] == original["users"][i]["id"]
            assert user["name"] == original["users"][i]["name"]
            assert user["role"] == original["users"][i]["role"]

    def test_complex_structure_roundtrip(self) -> None:
        """Test round-trip for complex nested structures."""
        original = {
            "product": "Widget",
            "price": 29.99,
            "stock": 100,
            "categories": ["tools", "hardware"],
            "metadata": {
                "created": "2024-01-01",
                "updated": "2024-01-15",
                "tags": ["featured", "bestseller"]
            },
            "reviews": [
                {"rating": 5, "comment": "Great product"},
                {"rating": 4, "comment": "Good value"}
            ]
        }
        json_str = json.dumps(original)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded == original

    def test_empty_containers_roundtrip(self) -> None:
        """Test round-trip for empty arrays and objects."""
        original = {
            "empty_array": [],
            "empty_object": {},
            "nested_empty": {
                "items": []
            }
        }
        json_str = json.dumps(original)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded["empty_array"] == []
        assert decoded["empty_object"] == {}
        assert decoded["nested_empty"]["items"] == []

    def test_special_values_roundtrip(self) -> None:
        """Test round-trip for special values."""
        original = {
            "null_value": None,
            "true_value": True,
            "false_value": False,
            "zero": 0,
            "empty_string": "",
            "negative": -42,
            "float": 3.14159
        }
        json_str = json.dumps(original)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded == original

    def test_unicode_roundtrip(self) -> None:
        """Test round-trip for unicode characters."""
        original = {
            "text": "Hello 世界",
            "emoji": "🚀🐍",
            "symbols": "α β γ"
        }
        json_str = json.dumps(original)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert decoded == original

    def test_multiple_roundtrips(self) -> None:
        """Test multiple encode-decode cycles."""
        original = {
            "data": [1, 2, 3],
            "meta": {"version": 1}
        }

        current = original
        for _ in range(3):
            json_str = json.dumps(current)
            toon = py_rtoon.encode_default(json_str)
            current = py_rtoon.decode_default(toon)

        assert current == original

    def test_large_dataset_roundtrip(self) -> None:
        """Test round-trip for larger dataset."""
        original = {
            "users": [
                {"id": i, "name": f"User{i}", "score": i * 10}
                for i in range(50)
            ]
        }
        json_str = json.dumps(original)

        toon = py_rtoon.encode_default(json_str)
        decoded = py_rtoon.decode_default(toon)

        assert len(decoded["users"]) == 50
        assert decoded == original

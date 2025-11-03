"""Basic encoding and decoding tests."""

import json
import pytest
import py_rtoon


class TestBasicEncoding:
    """Test basic encoding functionality."""

    def test_encode_simple_object(self) -> None:
        """Test encoding a simple object."""
        data = {"name": "Alice", "age": 30}
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "name: Alice" in toon
        assert "age: 30" in toon

    def test_encode_with_array(self) -> None:
        """Test encoding object with array."""
        data = {"tags": ["python", "rust", "toon"]}
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "tags[3]:" in toon
        assert "python,rust,toon" in toon

    def test_encode_nested_object(self) -> None:
        """Test encoding nested objects."""
        data = {
            "user": {
                "id": 123,
                "name": "Ada",
                "active": True
            }
        }
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "user:" in toon
        assert "id: 123" in toon
        assert "name: Ada" in toon
        assert "active: true" in toon

    def test_encode_tabular_data(self) -> None:
        """Test encoding array of objects (tabular format)."""
        data = {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "user"}
            ]
        }
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "users[2]{" in toon
        assert "id,name,role" in toon or "id,role,name" in toon

    def test_encode_empty_array(self) -> None:
        """Test encoding empty array."""
        data = {"items": []}
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "items[0]:" in toon

    def test_encode_boolean_values(self) -> None:
        """Test encoding boolean values."""
        data = {"active": True, "archived": False}
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "active: true" in toon
        assert "archived: false" in toon

    def test_encode_null_value(self) -> None:
        """Test encoding null values."""
        data = {"value": None}
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "value: null" in toon

    def test_encode_numbers(self) -> None:
        """Test encoding different number types."""
        data = {
            "integer": 42,
            "float": 3.14,
            "negative": -10
        }
        json_str = json.dumps(data)
        toon = py_rtoon.encode_default(json_str)

        assert "integer: 42" in toon
        assert "float: 3.14" in toon
        assert "negative: -10" in toon


class TestBasicDecoding:
    """Test basic decoding functionality."""

    def test_decode_simple_object(self) -> None:
        """Test decoding a simple object."""
        toon = "name: Alice\nage: 30"
        data = py_rtoon.decode_default(toon)

        assert data["name"] == "Alice"
        assert data["age"] == 30

    def test_decode_with_array(self) -> None:
        """Test decoding object with array."""
        toon = "tags[3]: python,rust,toon"
        data = py_rtoon.decode_default(toon)

        assert data["tags"] == ["python", "rust", "toon"]

    def test_decode_nested_object(self) -> None:
        """Test decoding nested objects."""
        toon = """user:
  id: 123
  name: Ada
  active: true"""
        data = py_rtoon.decode_default(toon)

        assert data["user"]["id"] == 123
        assert data["user"]["name"] == "Ada"
        assert data["user"]["active"] is True

    def test_decode_tabular_data(self) -> None:
        """Test decoding tabular format."""
        toon = """users[2]{id,name,role}:
  1,Alice,admin
  2,Bob,user"""
        data = py_rtoon.decode_default(toon)

        assert len(data["users"]) == 2
        assert data["users"][0]["id"] == 1
        assert data["users"][0]["name"] == "Alice"
        assert data["users"][1]["role"] == "user"

    def test_decode_empty_array(self) -> None:
        """Test decoding empty array."""
        toon = "items[0]:"
        data = py_rtoon.decode_default(toon)

        assert data["items"] == []

    def test_decode_boolean_values(self) -> None:
        """Test decoding boolean values."""
        toon = "active: true\narchived: false"
        data = py_rtoon.decode_default(toon)

        assert data["active"] is True
        assert data["archived"] is False

    def test_decode_null_value(self) -> None:
        """Test decoding null values."""
        toon = "value: null"
        data = py_rtoon.decode_default(toon)

        assert data["value"] is None


class TestInvalidInput:
    """Test error handling for invalid inputs."""

    def test_encode_invalid_json(self) -> None:
        """Test encoding with invalid JSON."""
        with pytest.raises(ValueError, match="Invalid JSON"):
            py_rtoon.encode_default("{invalid json}")

    def test_decode_invalid_toon(self) -> None:
        """Test decoding with malformed TOON."""
        with pytest.raises(ValueError, match="Decoding failed"):
            py_rtoon.decode_default("invalid[toon]format{}")

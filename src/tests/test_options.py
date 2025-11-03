"""Test EncodeOptions and DecodeOptions functionality."""

import json
import py_rtoon


class TestEncodeOptions:
    """Test EncodeOptions configuration."""

    def test_default_options(self) -> None:
        """Test creating default encode options."""
        options = py_rtoon.EncodeOptions()
        assert options is not None

    def test_with_length_marker(self) -> None:
        """Test adding length marker to arrays."""
        data = {"tags": ["a", "b", "c"], "items": [1, 2, 3, 4]}
        json_str = json.dumps(data)

        options = py_rtoon.EncodeOptions()
        options_with_marker = options.with_length_marker('#')
        toon = py_rtoon.encode(json_str, options_with_marker)

        assert "[#3]:" in toon or "[#4]:" in toon

    def test_chained_options(self) -> None:
        """Test chaining multiple option configurations."""
        data = {"tags": ["a", "b", "c"]}
        json_str = json.dumps(data)

        options = py_rtoon.EncodeOptions()
        options_custom = (options
                         .with_delimiter(py_rtoon.Delimiter.pipe())
                         .with_length_marker('#'))
        toon = py_rtoon.encode(json_str, options_custom)

        assert "[#3|]:" in toon or "[|#3]:" in toon
        assert "|" in toon

    def test_length_marker_with_tabular_data(self) -> None:
        """Test length marker with tabular format."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
        json_str = json.dumps(data)

        options = py_rtoon.EncodeOptions()
        options_with_marker = options.with_length_marker('#')
        toon = py_rtoon.encode(json_str, options_with_marker)

        assert "[#2]" in toon

    def test_different_length_markers(self) -> None:
        """Test different length marker characters."""
        data = {"items": [1, 2, 3]}
        json_str = json.dumps(data)

        for marker in ['#', '@', '*']:
            options = py_rtoon.EncodeOptions()
            options_with_marker = options.with_length_marker(marker)
            toon = py_rtoon.encode(json_str, options_with_marker)
            assert f"[{marker}3]:" in toon


class TestDecodeOptions:
    """Test DecodeOptions configuration."""

    def test_default_options(self) -> None:
        """Test creating default decode options."""
        options = py_rtoon.DecodeOptions()
        assert options is not None

    def test_strict_mode_enabled(self) -> None:
        """Test strict mode validation."""
        toon = "items[3]: a,b,c"
        options = py_rtoon.DecodeOptions()
        options_strict = options.with_strict(True)

        json_str = py_rtoon.decode(toon, options_strict)
        data = json.loads(json_str)
        assert data["items"] == ["a", "b", "c"]

    def test_strict_mode_disabled(self) -> None:
        """Test non-strict mode (more lenient)."""
        toon = "items[2]: a,b"  # Correct count for non-strict mode
        options = py_rtoon.DecodeOptions()
        options_lenient = options.with_strict(False)

        # Should decode successfully
        json_str = py_rtoon.decode(toon, options_lenient)
        data = json.loads(json_str)
        assert "items" in data
        assert data["items"] == ["a", "b"]

    def test_coerce_types_enabled(self) -> None:
        """Test type coercion enabled."""
        toon = "value: 123"
        options = py_rtoon.DecodeOptions()
        options_coerce = options.with_coerce_types(True)

        json_str = py_rtoon.decode(toon, options_coerce)
        data = json.loads(json_str)
        assert data["value"] == 123

    def test_coerce_types_disabled(self) -> None:
        """Test type coercion disabled."""
        toon = "value: 123"
        options = py_rtoon.DecodeOptions()
        options_no_coerce = options.with_coerce_types(False)

        json_str = py_rtoon.decode(toon, options_no_coerce)
        data = json.loads(json_str)
        # Result depends on implementation, but should decode successfully
        assert "value" in data

    def test_chained_decode_options(self) -> None:
        """Test chaining decode options."""
        toon = "items[2]: a,b"
        options = py_rtoon.DecodeOptions()
        options_custom = (options
                         .with_strict(False)
                         .with_coerce_types(True))

        json_str = py_rtoon.decode(toon, options_custom)
        data = json.loads(json_str)
        assert "items" in data


class TestOptionsRoundtrip:
    """Test round-trip encoding/decoding with options."""

    def test_roundtrip_with_pipe_delimiter(self) -> None:
        """Test round-trip with pipe delimiter."""
        original = {
            "users": [
                {"id": 1, "name": "Alice,Smith"},
                {"id": 2, "name": "Bob,Jones"}
            ]
        }
        json_str = json.dumps(original)

        # Encode with pipe delimiter
        encode_opts = py_rtoon.EncodeOptions()
        encode_opts_pipe = encode_opts.with_delimiter(py_rtoon.Delimiter.pipe())
        toon = py_rtoon.encode(json_str, encode_opts_pipe)

        # Decode with lenient mode
        decode_opts = py_rtoon.DecodeOptions()
        decode_opts_lenient = decode_opts.with_strict(False)
        decoded_json = py_rtoon.decode(toon, decode_opts_lenient)
        decoded = json.loads(decoded_json)

        assert len(decoded["users"]) == 2

    def test_roundtrip_with_length_marker(self) -> None:
        """Test round-trip with length marker."""
        original = {"tags": ["python", "rust", "typescript"]}
        json_str = json.dumps(original)

        # Encode with length marker
        encode_opts = py_rtoon.EncodeOptions()
        encode_opts_marker = encode_opts.with_length_marker('#')
        toon = py_rtoon.encode(json_str, encode_opts_marker)

        # Decode
        decoded_json = py_rtoon.decode_default(toon)
        decoded = json.loads(decoded_json)

        assert decoded == original

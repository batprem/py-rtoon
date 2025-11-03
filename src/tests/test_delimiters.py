"""Test custom delimiter functionality."""

import json
import py_rtoon


class TestDelimiters:
    """Test different delimiter options."""

    def test_comma_delimiter(self) -> None:
        """Test comma delimiter (default)."""
        data = {"tags": ["a", "b", "c"]}
        json_str = json.dumps(data)

        options = py_rtoon.EncodeOptions()
        options_with_comma = options.with_delimiter(py_rtoon.Delimiter.comma())
        toon = py_rtoon.encode(json_str, options_with_comma)

        assert "tags[3]: a,b,c" in toon

    def test_pipe_delimiter(self) -> None:
        """Test pipe delimiter."""
        data = {"tags": ["a", "b", "c"]}
        json_str = json.dumps(data)

        options = py_rtoon.EncodeOptions()
        options_with_pipe = options.with_delimiter(py_rtoon.Delimiter.pipe())
        toon = py_rtoon.encode(json_str, options_with_pipe)

        assert "tags[3|]: a|b|c" in toon

    def test_tab_delimiter(self) -> None:
        """Test tab delimiter."""
        data = {"tags": ["a", "b", "c"]}
        json_str = json.dumps(data)

        options = py_rtoon.EncodeOptions()
        options_with_tab = options.with_delimiter(py_rtoon.Delimiter.tab())
        toon = py_rtoon.encode(json_str, options_with_tab)

        assert "tags[3\t]:" in toon
        assert "\t" in toon

    def test_pipe_delimiter_with_commas_in_data(self) -> None:
        """Test pipe delimiter when data contains commas."""
        data = {"items": ["item,1", "item,2", "item,3"]}
        json_str = json.dumps(data)

        # Use pipe delimiter to avoid quoting
        options = py_rtoon.EncodeOptions()
        options_with_pipe = options.with_delimiter(py_rtoon.Delimiter.pipe())
        toon = py_rtoon.encode(json_str, options_with_pipe)

        assert "|" in toon

    def test_delimiter_in_tabular_data(self) -> None:
        """Test delimiter in tabular format."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
        json_str = json.dumps(data)

        options = py_rtoon.EncodeOptions()
        options_with_pipe = options.with_delimiter(py_rtoon.Delimiter.pipe())
        toon = py_rtoon.encode(json_str, options_with_pipe)

        assert "|" in toon
        assert "Alice" in toon and "Bob" in toon

    def test_delimiter_roundtrip(self) -> None:
        """Test round-trip with different delimiters."""
        data = {"tags": ["x", "y", "z"], "count": 3}
        json_str = json.dumps(data)

        # Encode with pipe delimiter
        options = py_rtoon.EncodeOptions()
        options_with_pipe = options.with_delimiter(py_rtoon.Delimiter.pipe())
        toon = py_rtoon.encode(json_str, options_with_pipe)

        # Decode back
        decoded = py_rtoon.decode_default(toon)

        assert decoded == data

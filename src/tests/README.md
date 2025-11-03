# py-rtoon Test Suite

Comprehensive test suite for py-rtoon Python bindings.

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest src/tests/test_basic.py

# Run specific test class
uv run pytest src/tests/test_basic.py::TestBasicEncoding

# Run specific test
uv run pytest src/tests/test_basic.py::TestBasicEncoding::test_encode_simple_object

# Run with coverage (if installed)
uv run pytest --cov=py_rtoon --cov-report=html
```

## Test Structure

### test_basic.py (17 tests)
Tests basic encoding and decoding functionality:
- Simple objects
- Nested objects
- Arrays
- Tabular data
- Empty containers
- Boolean and null values
- Number types
- Invalid input handling

### test_delimiters.py (6 tests)
Tests custom delimiter functionality:
- Comma delimiter (default)
- Pipe delimiter
- Tab delimiter
- Delimiter handling with special characters
- Delimiter in tabular format
- Round-trip with delimiters

### test_options.py (13 tests)
Tests EncodeOptions and DecodeOptions:
- Default options creation
- Length markers
- Chained options
- Strict mode
- Type coercion
- Round-trip with custom options

### test_roundtrip.py (10 tests)
Tests round-trip encoding and decoding:
- Simple and nested objects
- Arrays and tabular data
- Complex nested structures
- Empty containers
- Special values
- Unicode characters
- Multiple round-trip cycles
- Large datasets

### test_edge_cases.py (16 tests)
Tests edge cases and boundary conditions:
- Very long strings
- Deeply nested structures
- Many keys
- Large arrays
- Special characters in keys and values
- Mixed type arrays
- Numeric edge values
- Whitespace handling
- Empty string keys
- Error recovery

## Test Coverage

Total tests: **62**

Coverage by category:
- Basic functionality: 17 tests
- Delimiter handling: 6 tests
- Options configuration: 13 tests
- Round-trip conversion: 10 tests
- Edge cases: 16 tests

## Writing New Tests

When adding new tests:

1. Follow existing test structure and naming conventions
2. Use type hints (Python 3.11+ style)
3. Add descriptive docstrings
4. Group related tests in classes
5. Use fixtures from `conftest.py` when appropriate

Example:

```python
def test_new_feature(self) -> None:
    """Test description here."""
    data = {"key": "value"}
    json_str = json.dumps(data)

    toon = py_rtoon.encode_default(json_str)
    decoded_json = py_rtoon.decode_default(toon)
    decoded = json.loads(decoded_json)

    assert decoded == data
```

## Continuous Integration

Tests should pass before merging any pull requests. Run the full test suite:

```bash
uv run pytest -v
```

All 62 tests should pass with no failures.

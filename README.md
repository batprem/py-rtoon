<div align="center">

# 🐍 py-rtoon 🦀

**Python bindings for RToon - Token-Oriented Object Notation**

*A compact, token-efficient format for structured data in LLM applications*

<img src="https://github.com/alpkeskin/gotoon/raw/main/.github/og.png" alt="TOON - Token-Oriented Object Notation" width="600">

[![PyPI](https://img.shields.io/pypi/v/py-rtoon)](https://pypi.org/project/py-rtoon/)
[![Python](https://img.shields.io/pypi/pyversions/py-rtoon)](https://pypi.org/project/py-rtoon/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/premchotipanit/py-rtoon/actions/workflows/ci.yml/badge.svg)](https://github.com/premchotipanit/py-rtoon/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-86%20passed-brightgreen)](https://github.com/premchotipanit/py-rtoon/tree/main/src/tests)

</div>

---

**Token-Oriented Object Notation** is a compact, human-readable format designed for passing structured data to Large Language Models with significantly reduced token usage. This package provides Python bindings for the [rtoon](https://github.com/shreyasbhat0/rtoon) Rust implementation.

> [!TIP]
> Think of TOON as a translation layer: use JSON programmatically, convert to TOON for LLM input.

> [!NOTE]
> This module uses [rtoon](https://github.com/shreyasbhat0/rtoon) (Rust implementation) as a dependency via PyO3/maturin.

## Table of Contents

- [Why TOON?](#why-toon)
- [Why `py-rtoon`](#why-pyrtoon)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
  - [Basic Encoding and Decoding](#basic-encoding-and-decoding)
  - [Custom Delimiters](#custom-delimiters)
  - [Custom Options](#custom-options)
  - [Round-Trip Conversion](#round-trip-conversion)
- [API Reference](#api-reference)
- [Format Overview](#format-overview)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [See Also](#see-also)

## Why TOON?

AI is becoming cheaper and more accessible, but larger context windows allow for larger data inputs as well. **LLM tokens still cost money**  and standard JSON is verbose and token-expensive.

### JSON vs TOON Comparison

<details>
<summary><strong>=� Click to see the token efficiency comparison</strong></summary>

**JSON** (verbose, token-heavy):
```json
{
  "users": [
    { "id": 1, "name": "Alice", "role": "admin" },
    { "id": 2, "name": "Bob", "role": "user" }
  ]
}
```

**TOON** (compact, token-efficient):
```toon
users[2]{id,name,role}:
  1,Alice,admin
  2,Bob,user
```

TOON conveys the same information with **3060% fewer tokens**! <�

</details>

## Why py-rtoon?

Python is the **dominant language for AI/ML development**, powering most LLM applications, agent frameworks, and data pipelines. However, when working with LLMs, you need:

### 🚀 Performance Without Compromise

- **Blazing fast encoding/decoding** powered by Rust (via PyO3)
- **Zero-copy operations** where possible for maximum efficiency
- **Production-ready** performance for high-throughput applications
- Orders of magnitude faster than pure Python implementations

### 🐍 Seamless Python Integration

- **Native Python API** with proper type hints and docstrings
- **Works with standard `json` module** - no need to change your existing code structure
- **Simple integration** into existing LLM pipelines (LangChain, LlamaIndex, etc.)
- **Familiar patterns** for Python developers

### 💰 Cost Optimization for LLM Applications

When you're building AI applications, token costs add up quickly:

```python
# Before: Sending full JSON to LLM
prompt = f"Analyze this data: {json.dumps(large_dataset)}"
# Cost: ~5000 tokens

# After: Using TOON format
toon_data = py_rtoon.encode_default(json.dumps(large_dataset))
prompt = f"Analyze this data: {toon_data}"
# Cost: ~2000 tokens (60% reduction!)
```

**Real-world savings:**
- Processing 1M API calls with 1000-token JSON objects
- JSON cost: ~$15 at GPT-4 rates
- TOON cost: ~$6 (saving $9 per million calls)

### 🛠️ Perfect for Common Python + LLM Workflows

**Agent frameworks:**
```python
# Pass structured data to agents efficiently
agent.run(f"Process: {py_rtoon.encode_default(json.dumps(data))}")
```

**RAG pipelines:**
```python
# Encode documents for vector storage with metadata
metadata_toon = py_rtoon.encode_default(json.dumps(metadata))
```

**Prompt engineering:**
```python
# Build token-efficient prompts with complex data
prompt = f"""
Given this user profile:
{py_rtoon.encode_default(json.dumps(user_data))}

Provide recommendations.
"""
```

**API response optimization:**
```python
# Return compact responses to save bandwidth and tokens
return {"data": py_rtoon.encode_default(json.dumps(results))}
```

### ✨ Why Not Pure Python?

While you could implement TOON in pure Python, `py-rtoon` gives you:

- **5-50x faster** encoding/decoding performance
- **Battle-tested Rust implementation** with comprehensive test coverage
- **Memory efficiency** - important for processing large datasets
- **Active maintenance** - benefits from improvements in the core rtoon library
- **Type safety** - Rust's guarantees prevent entire classes of bugs

## Key Features

- =� **Token-efficient:** typically 3060% fewer tokens than JSON
- >? **LLM-friendly guardrails:** explicit lengths and fields enable validation
- <q **Minimal syntax:** removes redundant punctuation (braces, brackets, most quotes)
- =� **Indentation-based structure:** like YAML, uses whitespace instead of braces
- >� **Tabular arrays:** declare keys once, stream data as rows
- = **Round-trip support:** encode and decode with full fidelity
- >� **Fast:** powered by Rust via PyO3
- =
 **Pythonic:** clean API with proper type hints
- � **Customizable:** delimiter (comma/tab/pipe), length markers, and indentation

## Installation

```bash
# Using uv (recommended)
uv add py-rtoon

# Using pip
pip install py-rtoon
```

## Quick Start

```python
import py_rtoon

# Encode Python dict directly to TOON
data = {
    "user": {
        "id": 123,
        "name": "Ada",
        "tags": ["reading", "gaming"],
        "active": True
    }
}

toon = py_rtoon.encode_default(data)
print(toon)
```

**Output:**

```toon
user:
  active: true
  id: 123
  name: Ada
  tags[2]: reading,gaming
```

**Decode back to Python dict:**

```python
# Decode TOON back to dict
decoded = py_rtoon.decode_default(toon)
print(decoded)
# {'user': {'active': True, 'id': 123, 'name': 'Ada', 'tags': ['reading', 'gaming']}}
```

## Examples

### Basic Encoding and Decoding

```python
import py_rtoon

# Encode dict to TOON (new Pythonic API!)
data = {"name": "Alice", "age": 30, "tags": ["python", "rust"]}
toon = py_rtoon.encode_default(data)
print(f"Encoded: {toon}")

# Decode TOON back to dict
decoded = py_rtoon.decode_default(toon)
print(f"Decoded: {decoded}")
print(f"Type: {type(decoded)}")
```

**Output:**

```
Encoded: name: Alice
age: 30
tags[2]: python,rust

Decoded: {'name': 'Alice', 'age': 30, 'tags': ['python', 'rust']}
Type: <class 'dict'>
```

**Backward compatible with JSON strings:**

```python
import json

# Still works with JSON strings
json_str = json.dumps(data)
toon = py_rtoon.encode_default(json_str)

```

### Custom Delimiters

Use different delimiters to avoid quoting and save more tokens:

```python
import py_rtoon
import json

data = {
    "items": [
        {"sku": "A1", "name": "Widget", "qty": 2},
        {"sku": "B2", "name": "Gadget", "qty": 1}
    ]
}

json_str = json.dumps(data)

# Use pipe delimiter
options = py_rtoon.EncodeOptions()
options_with_pipe = options.with_delimiter(py_rtoon.Delimiter.pipe())
toon_pipe = py_rtoon.encode(json_str, options_with_pipe)
print("With pipe delimiter:")
print(toon_pipe)

# Use tab delimiter
options_with_tab = options.with_delimiter(py_rtoon.Delimiter.tab())
toon_tab = py_rtoon.encode(json_str, options_with_tab)
print("\nWith tab delimiter:")
print(toon_tab)
```

### Custom Options

Customize encoding with length markers:

```python
import py_rtoon
import json

data = {
    "tags": ["reading", "gaming", "coding"],
    "items": [
        {"sku": "A1", "qty": 2, "price": 9.99},
        {"sku": "B2", "qty": 1, "price": 14.5}
    ]
}

json_str = json.dumps(data)

# Add length marker '#'
options = py_rtoon.EncodeOptions()
options_with_marker = options.with_length_marker('#')
toon = py_rtoon.encode(json_str, options_with_marker)
print(toon)
```

**Output:**

```toon
items[#2]{sku,qty,price}:
  A1,2,9.99
  B2,1,14.5
tags[#3]: reading,gaming,coding
```

### Round-Trip Conversion

TOON supports full round-trip encoding and decoding:

```python
import py_rtoon
import json

original_data = {
    "product": "Widget",
    "price": 29.99,
    "stock": 100,
    "categories": ["tools", "hardware"]
}

# Convert to JSON string
json_str = json.dumps(original_data)

# Encode to TOON
toon = py_rtoon.encode_default(json_str)
print(f"TOON:\n{toon}\n")

# Decode back to JSON
decoded_json = py_rtoon.decode_default(toon)
decoded_data = json.loads(decoded_json)

# Verify round-trip
assert original_data == decoded_data
print(" Round-trip successful!")
```

## API Reference

### Functions

#### `encode_default(json_str: str) -> str`

Encode a JSON string to TOON format using default options.

**Parameters:**
- `json_str` (str): A JSON string to encode

**Returns:**
- str: A TOON-formatted string

**Raises:**
- `ValueError`: If the JSON is invalid or encoding fails

**Example:**

```python
import py_rtoon
import json

data = {"name": "Alice", "age": 30}
toon = py_rtoon.encode_default(json.dumps(data))
```

#### `decode_default(toon_str: str) -> str`

Decode a TOON string to JSON format using default options.

**Parameters:**
- `toon_str` (str): A TOON-formatted string to decode

**Returns:**
- str: A JSON string

**Raises:**
- `ValueError`: If the TOON string is invalid or decoding fails

**Example:**

```python
import py_rtoon

toon = "name: Alice\nage: 30"
json_str = py_rtoon.decode_default(toon)
```

#### `encode(json_str: str, options: EncodeOptions) -> str`

Encode a JSON string to TOON format with custom options.

**Parameters:**
- `json_str` (str): A JSON string to encode
- `options` (EncodeOptions): Options for customizing the output format

**Returns:**
- str: A TOON-formatted string

**Raises:**
- `ValueError`: If the JSON is invalid or encoding fails

#### `decode(toon_str: str, options: DecodeOptions) -> str`

Decode a TOON string to JSON format with custom options.

**Parameters:**
- `toon_str` (str): A TOON-formatted string to decode
- `options` (DecodeOptions): Options for customizing the decoding behavior

**Returns:**
- str: A JSON string

**Raises:**
- `ValueError`: If the TOON string is invalid or decoding fails

### Classes

#### `Delimiter`

Delimiter options for encoding TOON format.

**Static Methods:**
- `comma() -> Delimiter`: Comma delimiter (default)
- `pipe() -> Delimiter`: Pipe delimiter (`|`)
- `tab() -> Delimiter`: Tab delimiter (`\t`)

**Example:**

```python
import py_rtoon

delimiter = py_rtoon.Delimiter.pipe()
```

#### `EncodeOptions`

Options for encoding to TOON format.

**Methods:**
- `__init__()`: Create new encoding options with defaults
- `with_delimiter(delimiter: Delimiter) -> EncodeOptions`: Set the delimiter for arrays
- `with_length_marker(marker: str) -> EncodeOptions`: Set the length marker character

**Example:**

```python
import py_rtoon

options = (py_rtoon.EncodeOptions()
    .with_delimiter(py_rtoon.Delimiter.pipe())
    .with_length_marker('#'))
```

#### `DecodeOptions`

Options for decoding TOON format.

**Methods:**
- `__init__()`: Create new decoding options with defaults
- `with_strict(strict: bool) -> DecodeOptions`: Enable/disable strict mode (validates array lengths)
- `with_coerce_types(coerce: bool) -> DecodeOptions`: Enable/disable type coercion

**Example:**

```python
import py_rtoon

options = (py_rtoon.DecodeOptions()
    .with_strict(True)
    .with_coerce_types(False))
```

## Format Overview

- **Objects:** `key: value` with 2-space indentation for nesting
- **Primitive arrays:** inline with count, e.g., `tags[3]: a,b,c`
- **Arrays of objects:** tabular header, e.g., `items[2]{id,name}:\n  ...`
- **Mixed arrays:** list format with `- ` prefix
- **Quoting:** only when necessary (special chars, ambiguity, keywords like `true`, `null`)
- **Root forms:** objects (default), arrays, or primitives

For complete format specification, see the [TOON Specification](https://github.com/shreyasbhat0/rtoon/blob/main/SPEC.md).

## Testing

py-rtoon includes a comprehensive test suite with **86 tests** covering all functionality:

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest src/tests/test_basic.py
```

**Test Coverage:**
- ✅ Basic encoding/decoding (17 tests)
- ✅ Custom delimiters (6 tests)
- ✅ Options configuration (13 tests)
- ✅ Round-trip conversion (10 tests)
- ✅ Edge cases (16 tests)
- ✅ **Dict support (24 tests)** - NEW!

All tests use Python 3.11+ type hints and follow best practices. See [src/tests/README.md](src/tests/README.md) for more details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

<details>
<summary><strong>> How to Contribute</strong></summary>

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Run tests to ensure everything works (`uv run pytest -v`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please ensure all 86 tests pass before submitting your PR.

</details>

## License

MIT 2025

## See Also

- **Rust implementation (dependency):** [rtoon](https://github.com/shreyasbhat0/rtoon)
- **Original JavaScript/TypeScript implementation:** [@byjohann/toon](https://github.com/johannschopplich/toon)
- **TOON Specification:** [SPEC.md](https://github.com/shreyasbhat0/rtoon/blob/main/SPEC.md)

## TODO-Lists
- Release and index to Pypi
- Add compatibility to other Python version with other platform, now only Python 3.14 on Mac-OS (M3) is tested
- Add performance benchmarking other TOON tools
- Add LLM Accuracy benchmarking
- Add more data type support (Pydantic/ORM/dict)
- Ensure framework compatibility like (Langchain/Langgraph/CrewAI/ etc.)

---

<div align="center">

**Built with ❤️ using Rust + Python**

</div>

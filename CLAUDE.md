# General rules
- Contents in rtoon/ are read only

# Python rules
- Don't typing with `from typing import Dict, Optional, List` instead follow 3.11+ typing style
- Avoid `Any` type as much as possible
- Using `pydantic` is preferred more than using plain `dict`
- Don't use `pip install` to install a new module, use `uv add` instead

# Goal of the project
- This project is to create a Python module that can Rust `rtoon` functions by `maturin`
"""Pytest configuration and fixtures for py-rtoon tests."""

import pytest


@pytest.fixture
def sample_simple_data() -> dict[str, str | int]:
    """Provide simple test data."""
    return {"name": "Alice", "age": 30}


@pytest.fixture
def sample_nested_data() -> dict[str, dict[str, str | int | bool]]:
    """Provide nested test data."""
    return {
        "user": {
            "id": 123,
            "name": "Ada",
            "active": True
        }
    }


@pytest.fixture
def sample_array_data() -> dict[str, list[str]]:
    """Provide array test data."""
    return {"tags": ["python", "rust", "typescript"]}


@pytest.fixture
def sample_tabular_data() -> dict[str, list[dict[str, str | int]]]:
    """Provide tabular test data."""
    return {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "guest"}
        ]
    }


@pytest.fixture
def sample_complex_data() -> dict[str, str | float | int | list | dict]:
    """Provide complex nested test data."""
    return {
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
            {"rating": 5, "comment": "Great"},
            {"rating": 4, "comment": "Good"}
        ]
    }

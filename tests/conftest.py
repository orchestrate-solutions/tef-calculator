"""
Pytest configuration and shared fixtures for calculator tests.
"""
import pytest
from codeuchain.core import Context


@pytest.fixture
def sample_context():
    """Provide a basic context for testing."""
    return Context({})


@pytest.fixture
def add_context():
    """Provide a context for addition operations."""
    return Context({"operation": "add", "operands": [5, 3]})


@pytest.fixture
def subtract_context():
    """Provide a context for subtraction operations."""
    return Context({"operation": "subtract", "operands": [10, 4]})


@pytest.fixture
def multiply_context():
    """Provide a context for multiplication operations."""
    return Context({"operation": "multiply", "operands": [6, 7]})


@pytest.fixture
def divide_context():
    """Provide a context for division operations."""
    return Context({"operation": "divide", "operands": [20, 4]})

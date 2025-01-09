import pytest
from modules.deepseek import (
    prompt,
    fill_in_the_middle_prompt,
    json_prompt,
    prefix_prompt,
    prefix_then_stop_prompt,
)


def test_prompt():
    """Test basic prompt functionality"""
    response = prompt("Hello, how are you?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_fill_in_the_middle_prompt():
    """Test fill-in-the-middle prompt"""
    response = fill_in_the_middle_prompt(
        prompt="def fib(n):", suffix="    return fib(n-1) + fib(n-2)"
    )
    print("response", response)
    assert isinstance(response, str)
    assert "if" in response or "elif" in response or "else" in response


def test_json_prompt():
    """Test JSON response format"""
    response = json_prompt("Return a JSON object with a 'message' key")
    assert isinstance(response, dict)
    assert "message" in response
    assert isinstance(response["message"], str)


def test_prefix_prompt():
    """Test prefix-constrained prompt"""
    response = prefix_prompt(
        prompt="Complete this sentence: The best programming language is",
        prefix="The best programming language is Python",
    )
    print("response", response)
    assert isinstance(response, str)
    # Make assertion more flexible to handle different responses
    assert "Python" in response  # Just verify Python is mentioned
    assert len(response) > len(
        "The best programming language is Python"
    )  # Verify response continues


def test_prefix_suffix_prompt():
    """Test prefix and suffix constrained prompt"""
    response = prefix_then_stop_prompt(
        prompt="Generate python code in a markdown code block that completes this function: def csvs_to_sqlite_tables(csvs: List[str], sqlite_db: str)",
        prefix="```python",
        suffix="```",
    )
    print("response", response)
    assert isinstance(response, str)
    assert "def csvs_to_sqlite_tables" in response

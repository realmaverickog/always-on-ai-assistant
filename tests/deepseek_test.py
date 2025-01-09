import pytest
from modules.deepseek import (
    prompt,
    fill_in_the_middle_prompt,
    json_prompt,
    prefix_prompt,
    prefix_suffix_prompt,
)

def test_prompt():
    """Test basic prompt functionality"""
    response = prompt("Hello, how are you?")
    assert isinstance(response, str)
    assert len(response) > 0

def test_fill_in_the_middle_prompt():
    """Test fill-in-the-middle prompt"""
    response = fill_in_the_middle_prompt(
        prompt="def fib(n):",
        suffix="    return fib(n-1) + fib(n-2)"
    )
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
        prefix="The best programming language is Python"
    )
    assert isinstance(response, str)
    assert response.startswith("The best programming language is Python")

def test_prefix_suffix_prompt():
    """Test prefix and suffix constrained prompt"""
    response = prefix_suffix_prompt(
        prompt="Write a short poem about AI",
        prefix="In the world of ones and zeros",
        suffix="The future is bright with AI"
    )
    assert isinstance(response, str)
    assert response.startswith("In the world of ones and zeros")
    assert "The future is bright with AI" not in response  # Should stop before suffix

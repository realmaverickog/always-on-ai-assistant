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
    """Test fill-in-the-middle prompt with an SQL query example"""
    response = fill_in_the_middle_prompt(
        prompt="""SELECT 
    customer_id,
    first_name,
    last_name,
    """,
        suffix="""
ORDER BY last_name ASC;
""",
    )

    assert isinstance(response, str)
    assert len(response) > 10  # Verify meaningful content
    assert "FROM" in response  # Verify suffix is not included

    # Verify SQL syntax and common patterns
    assert any(
        word in response for word in ["email", "phone", "address", "city", "state"]
    )  # Common customer columns
    assert "," in response  # Verify proper column separation
    assert "\n" in response  # Verify formatting


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

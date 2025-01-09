import pytest
from modules.execute_python import execute, execute_uv_python
import tempfile
import os


def test_execute_basic_command():
    """Test basic command execution"""
    result = execute("echo Hello World")
    assert "Hello World" in result
    assert len(result.strip()) > 0


def test_execute_error_command():
    """Test command execution with error"""
    result = execute("false")
    assert not result  # Should have some error output


def test_execute_uv_python_with_file(tmp_path):
    """Test uv python execution with a temporary python file"""
    # Create temporary python file
    test_file = tmp_path / "test_script.py"
    test_file.write_text("print('Hello from temp file')")

    # Execute the file
    result = execute_uv_python("", str(test_file))
    assert "Hello from temp file" in result


def test_execute_uv_python_with_args(tmp_path):
    """Test uv python execution with arguments"""
    # Create temporary python file
    test_file = tmp_path / "test_script.py"
    test_file.write_text(
        """
import sys
print(f'Arguments: {sys.argv[1:]}')
"""
    )

    # Execute with arguments
    result = execute_uv_python("arg1 arg2", str(test_file))
    assert "Arguments: ['arg1', 'arg2']" in result


def test_execute_uv_python_error(tmp_path):
    """Test uv python execution with error"""
    # Create temporary python file with error
    test_file = tmp_path / "test_script.py"
    test_file.write_text("raise ValueError('Test error')")

    # Execute and check for error
    result = execute_uv_python("", str(test_file))
    assert "ValueError" in result
    assert "Test error" in result

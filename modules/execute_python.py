import subprocess
import shlex


def execute_uv_python(command: str, file_path: str) -> str:
    """Execute the tests and return the output as a string."""
    complete_command = f"uv run python {file_path} {command}"

    return execute(complete_command)


def execute(command: str) -> str:
    """Execute shell code and return the output as a string."""
    result = subprocess.run(
        shlex.split(command),
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr

import os
import subprocess
from subprocess import CompletedProcess
import error_handler
from validate_directory import is_valid_directory

def run_command(command: list[str], cwd: str) -> CompletedProcess | None:
    """Runs the specified command and returns the result. Raises on failure."""

    if not is_valid_directory(cwd):
        
        return None

    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
        return result
    except Exception as e:
        error_handler.report_error("Run Command Exception", str(e))
        raise


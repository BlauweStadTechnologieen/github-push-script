import os
import subprocess
from subprocess import CompletedProcess
import error_handler

def run_command(command: list[str], cwd: str) -> CompletedProcess:
    """Runs the specified command and returns the result. Raises on failure."""

    if not os.path.exists(cwd):
        msg = f"The directory '{cwd}' does not exist."
        error_handler.report_error("Directory Error", msg)
        raise FileNotFoundError(msg)

    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
        return result
    except Exception as e:
        error_handler.report_error("Run Command Exception", str(e))
        raise


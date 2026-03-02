import logging
import subprocess
from subprocess import CompletedProcess
from error_handler import status_logger
from validate_directory import is_valid_directory

logger = logging.getLogger(__name__)

def run_command(command: list[str], cwd: str) -> CompletedProcess | None:
    """
    Executes a shell command in the specified working directory.
    Args:
        command (list[str]): The command and its arguments to execute as a list of strings.
        cwd (str): The working directory in which to run the command.
    Returns:
        CompletedProcess | None: The result of the executed command as a CompletedProcess object,
        or None if the specified directory is invalid.
    Raises:
        Exception: Propagates any exception encountered during command execution after reporting it.
    Notes:
        - If the provided working directory is not valid, the function returns None.
        - Errors encountered during execution are reported using the error_handler before being raised.
    """
    """Runs the specified command and returns the result. Raises on failure."""

    if not is_valid_directory(cwd):
        
        return None

    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)

        if result.returncode != 0:

            status_logger("Command Failed!", f"Command: {' '.join(command)}\nReturn Code: {result.returncode}\nStderr: {result.stderr}", logging_level=logging.ERROR)
            
            raise subprocess.CalledProcessError(

                result.returncode, command, output=result.stdout, stderr=result.stderr

            )
        
        return result
    
    except Exception as e:

        status_logger("Run Command Exception", str(e), logging_level=logging.ERROR)

        raise
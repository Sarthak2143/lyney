import subprocess
from pathlib import Path

from google.genai import types

from config import TIMEOUT_SECS
from functions.utils import validate_path


def run_python_file(
  working_dir: str, file_path: str, args: list[str] | None = None
) -> str:
  if not file_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file.'

  validation: Path | None = validate_path(working_dir, file_path)
  if not validation:
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

  full_path: Path = validation
  abs_wrk_dir: Path = Path(working_dir).resolve()

  if not full_path.exists():
    return f'Error: File "{file_path}" not found.'

  try:
    commands: list[str] = ["python3", str(full_path)]
    if args:
      commands.extend(args)
    result: subprocess.CompletedProcess[str] = subprocess.run(
      commands,
      capture_output=True,
      text=True,
      timeout=TIMEOUT_SECS,
      cwd=str(abs_wrk_dir),
    )
    output: list[str] = []
    if result.stdout:
      output.append(f"STDOUT: \n{result.stdout}")
    if result.stderr:
      output.append(f"STDERR: \n{result.stderr}")

    if result.returncode != 0:
      output.append(f"Process exited with code {result.returncode}")

    return "\n".join(output) if output else "No output produced."
  except subprocess.TimeoutExpired:
    return f"Error: Execution of {file_path} timed out after {TIMEOUT_SECS} seconds."
  except Exception as e:
    return f"Error: executing Python file: {e}"


schema_run_file: types.FunctionDeclaration = types.FunctionDeclaration(
  name="run_python_file",
  description="Executes a Python file within the working directory and returns the output from the interpreter.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Path to the Python file to execute, relative to the working directory.",
      ),
      "args": types.Schema(
        type=types.Type.ARRAY,
        items=types.Schema(
          type=types.Type.STRING,
          description="Optional arguments to pass to the python file.",
        ),
        description="Optional arguments to pass to the Python file.",
      ),
    },
    required=["file_path"],
  ),
)

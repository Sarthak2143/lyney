import os
import subprocess


def run_python_file(working_dir, file_path, args=[]) -> str:
  abs_wrk_dir = os.path.abspath(working_dir)
  full_path = os.path.abspath(os.path.join(working_dir, file_path))
  if not file_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file.'
  if not os.path.exists(full_path):
    return f'Error: File "{file_path}" not found.'
  if not full_path.startswith(abs_wrk_dir):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

  try:
    commands: list[str] = ["python3", file_path]
    if args:
      commands.extend(args)
    result = subprocess.run(
      commands,
      capture_output=True,
      text=True,
      timeout=30,
      cwd=abs_wrk_dir,
    )
    output: list[str] = []
    if result.stdout:
      output.append(f"STDOUT: \n{result.stdout}")
    if result.stderr:
      output.append(f"STDERR: \n{result.stderr}")

    if result.returncode != 0:
      output.append(f"Process exited with code {result.returncode}")

    return "\n".join(output) if output else "No output produced."
  except Exception as e:
    return f"Error: executing Python file: {e}"

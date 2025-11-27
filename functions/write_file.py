import os

from google.genai import types


def write_file(working_dir, file_path, content) -> str:
  abs_wrk_dir: str = os.path.abspath(working_dir)
  full_path: str = os.path.abspath(os.path.join(working_dir, file_path))
  if not full_path.startswith(abs_wrk_dir):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

  try:
    with open(full_path, "w") as f:
      f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f'Error writing file "{file_path}": {e}'


schema_write_file: types.FunctionDeclaration = types.FunctionDeclaration(
  name="write_file",
  description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Path to the file to write, relative to the working directory.",
      ),
      "content": types.Schema(
        type=types.Type.STRING, description="Content to write into the file."
      ),
    },
    required=["file_path", "content"],
  ),
)

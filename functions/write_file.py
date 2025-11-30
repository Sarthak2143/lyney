from pathlib import Path

from google.genai import types

from functions.utils import validate_path


def write_file(working_dir, file_path, content) -> str:
  validation: Path | None = validate_path(working_dir, file_path)
  if not validation:
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

  full_path: Path = validation

  try:
    # ensure parent dir exists
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
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

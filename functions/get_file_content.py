from google.genai import types
from pathlib import Path

from config import MAX_CHARS_TO_READ
from functions.utils import validate_path


def get_file_content(working_dir: str, file_path: str) -> str:
  validation: Path | None = validate_path(working_dir, file_path)
  if not validation:
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

  full_path: Path = validation

  if not full_path.is_file():
    return f'Error: File not found or is not a regular file: "{file_path}"'

  try:
    with open(full_path, "r", encoding="utf-8") as f:
      content: str = f.read(MAX_CHARS_TO_READ)
      if full_path.stat().st_size > MAX_CHARS_TO_READ:
        content += (
          f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ} characters]'
        )
    return content
  except Exception as e:
    return f'Error reading file "{file_path}": {e}'


schema_get_file_content: types.FunctionDeclaration = types.FunctionDeclaration(
  name="get_file_content",
  description=f"Read and returns the first {MAX_CHARS_TO_READ} characters of the content from a specified file within the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The file to get content from, relative to the working directory",
      )
    },
    required=["file_path"],
  ),
)

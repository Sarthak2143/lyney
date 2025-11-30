import os
from pathlib import Path

from google.genai import types

from functions.utils import validate_path


def get_files_info(working_dir: str, directory: str = ".") -> str:
  validation: Path | None = validate_path(working_dir, directory)
  if not validation:
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

  full_path: Path = validation

  if not full_path.is_dir():
    return f'Error: "{directory}" is not a directory'
  try:
    file_stats: list[str] = []
    for item in full_path.iterdir():
      stat: os.stat_result = item.stat()
      # building string to make debugging ez for llm
      file_stats.append(
        f"- {item.name}: file_size={stat.st_size} bytes, is_dir={item.is_dir()}"
      )
    return "\n".join(file_stats)
  except Exception as e:
    return f"Error listing files: {e}"


schema_get_files_info: types.FunctionDeclaration = types.FunctionDeclaration(
  name="get_files_info",
  description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "directory": types.Schema(
        type=types.Type.STRING,
        description="The directory to list files from, relative to the working directory, lists files in the working directory itself.",
      )
    },
  ),
)

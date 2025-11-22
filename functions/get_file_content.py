import os

from config import MAX_CHARS_TO_READ


def get_file_content(working_dir, file_path) -> str:
  abs_wrk_dir = os.path.abspath(working_dir)
  full_path = os.path.abspath(os.path.join(working_dir, file_path))
  if not os.path.isfile(full_path):
    return f'Error: File not found or is not a regular file: "{file_path}"'
  if not full_path.startswith(abs_wrk_dir):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

  try:
    with open(full_path, "r") as f:
      content: str = f.read(MAX_CHARS_TO_READ)
      if os.path.getsize(full_path) > MAX_CHARS_TO_READ:
        content += (
          f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ} characters]'
        )
    return content
  except Exception as e:
    return f'Error reading file "{file_path}": {e}'

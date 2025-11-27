import os

from google.genai import types


def get_files_info(working_dir, directory=".") -> str:
  abs_wrk_dir: str = os.path.abspath(working_dir)
  full_path: str = os.path.abspath(os.path.join(working_dir, directory))
  if not os.path.isdir(full_path):
    return f'Error: "{directory}" is not a directory'
  # check if dir exists under working_dir
  if not full_path.startswith(abs_wrk_dir):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  try:
    file_stats: list[str] = []
    for file in os.listdir(full_path):
      file_path: str = os.path.join(full_path, file)
      # building string to make debugging ez for llm
      file_stats.append(
        f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
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

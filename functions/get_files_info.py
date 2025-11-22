import os


def get_files_info(working_dir, dir=".") -> str:
  abs_wrk_dir: str = os.path.abspath(working_dir)
  full_path: str = os.path.abspath(os.path.join(working_dir, dir))
  if not os.path.isdir(full_path):
    return f'Error: "{dir}" is not a directory'
  # check if dir exists under working_dir
  if not full_path.startswith(abs_wrk_dir):
    return (
      f'Error: Cannot list "{dir}" as it is outside the permitted working directory'
    )
  try:
    file_stats: list[str] = []
    for file in os.listdir(full_path):
      file_path = os.path.join(full_path, file)
      # building string to make debugging ez for llm
      file_stats.append(
        f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
      )
    return "\n".join(file_stats)
  except Exception as e:
    return f"Error listing files: {e}"

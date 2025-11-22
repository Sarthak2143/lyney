import os


def write_file(working_dir, file_path, content):
  abs_wrk_dir = os.path.abspath(working_dir)
  full_path = os.path.abspath(os.path.join(working_dir, file_path))
  if not full_path.startswith(abs_wrk_dir):
    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

  try:
    with open(full_path, "w") as f:
      f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f'Error writing file "{file_path}": {e}'

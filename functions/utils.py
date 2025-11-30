from pathlib import Path


def validate_path(working_dir: str, file_path: str) -> Path | None:
  """
  validates that a file path is within the workng_dir
  return (abs_wrk_dir, full_path) if valid else None
  """
  abs_wrk_dir: Path = Path(working_dir).resolve()
  full_path = (abs_wrk_dir / file_path).resolve()

  try:
    # check if path in wrk_dir
    full_path.relative_to(abs_wrk_dir)
    return full_path
  except ValueError:
    return None

from typing import Callable

from google.genai import types

from config import WORKING_DIR
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_file import run_python_file, schema_run_file
from functions.write_file import schema_write_file, write_file

available_functions: types.Tool = types.Tool(
  function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_file,
  ]
)


def call_function(
  function_call_part: types.FunctionCall, verbose=False
) -> types.Content:
  functions: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
  }
  if verbose:
    print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
  else:
    print(f" - Calling function: {function_call_part.name}")

  fn_name: str | None = function_call_part.name
  if fn_name not in functions:
    return types.Content(
      role="tool",
      parts=[
        types.Part.from_function_response(
          name=fn_name,  # pyright: ignore[reportArgumentType]
          response={"error": f"Unknown function: {fn_name}"},
        )
      ],
    )

  args: dict[bytes, bytes] = dict(function_call_part.args)  # pyright: ignore[reportCallIssue, reportArgumentType]
  args["working_dir"] = WORKING_DIR  # pyright: ignore[reportArgumentType]
  fn_result: str = functions[fn_name](**args)  # pyright: ignore[reportCallIssue]
  return types.Content(
    role="tool",
    parts=[
      types.Part.from_function_response(
        name=fn_name,
        response={"result": fn_result},
      )
    ],
  )

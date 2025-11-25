import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from schemas import available_functions, call_function


def main() -> None:
  load_dotenv()

  verbose: bool = "--verbose" in sys.argv
  args: list[str] = []
  for arg in sys.argv[1:]:
    if not arg.startswith("--"):
      args.append(arg)

  if not args:
    print(f'Usage: {sys.argv[0]} "prompt" [--verbose]')
    sys.exit(1)

  api_key: str | None = os.environ.get("GEMINI_API_KEY")
  client = genai.Client(api_key=api_key)

  prompt: str = " ".join(args)

  if verbose:
    print(f"User prompt: {prompt}")

  messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
  ]

  generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
  response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
      tools=[available_functions], system_instruction=system_prompt
    ),
  )
  if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")  # pyright: ignore[reportOptionalMemberAccess]
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")  # pyright: ignore[reportOptionalMemberAccess]

  if not response.function_calls:
    return response.text

  fn_resp: list[types.Part] = []
  for fn_call in response.function_calls:
    result: types.Content = call_function(fn_call, verbose)
    if not fn_call.parts or not result.parts[0].function_response:  # pyright: ignore[reportOptionalSubscript]
      raise Exception("empty function call result.")
    fn_resp.append(result.parts[0])  # pyright: ignore[reportOptionalSubscript]
    if verbose:
      print(f"-> {result.parts[0].function_response.response}")  # pyright: ignore[reportOptionalSubscript]

    if not fn_resp:
      raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
  main()

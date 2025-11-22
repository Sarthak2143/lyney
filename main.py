import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def exit_msg() -> None:
  print(f"Usage: {sys.argv[0]} prompt [--verbose]")
  sys.exit(1)


def main() -> None:
  if len(sys.argv) not in [2, 3]:
    exit_msg()
  verbose = False

  if len(sys.argv) == 3:
    if sys.argv[2] != "--verbose":
      exit_msg()
    else:
      verbose = True

  prompt: str = sys.argv[1]
  load_dotenv()
  api_key: str | None = os.environ.get("GEMINI_API_KEY")
  client = genai.Client(api_key=api_key)

  messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
  ]
  response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
  )
  print(response.text)
  if verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")  # pyright: ignore[reportOptionalMemberAccess]
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")  # pyright: ignore[reportOptionalMemberAccess]


if __name__ == "__main__":
  main()

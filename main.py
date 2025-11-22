import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


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


def generate_content(client, messages, verbose) -> None:
  response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
  )
  if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")  # pyright: ignore[reportOptionalMemberAccess]
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")  # pyright: ignore[reportOptionalMemberAccess]
  print("Reponse:")
  print(response.text)


if __name__ == "__main__":
  main()

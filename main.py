import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
  if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} prompt")
    sys.exit(1)

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
  print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")  # pyright: ignore[reportOptionalMemberAccess]
  print(f"Response tokens: {response.usage_metadata.candidates_token_count}")  # pyright: ignore[reportOptionalMemberAccess]


if __name__ == "__main__":
  main()

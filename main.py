import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import GEMINI_MODEL, HEADER, MAX_TRIES
from prompts import system_prompt
from schemas import available_functions, call_function


def main() -> None:
  load_dotenv()

  verbose: bool = "--verbose" in sys.argv

  api_key: str | None = os.environ.get("GEMINI_API_KEY")
  client: genai.Client = genai.Client(api_key=api_key)

  messages: list[types.Content] = []

  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")
  print(HEADER)
  print(" ai codihhn agent, so that you can goon rather than code")

  while True:
    try:
      prompt: str = input("> ").strip()
      if not prompt:
        continue
      if prompt.lower() in ("exit", "quit"):
        print("goodbye!")
        sys.exit(0)

      messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

      # retry loop
      last_error: Exception | None = None
      for attempt in range(1, MAX_TRIES + 1):
        try:
          res: str | None = generate_content(client, messages, verbose)
          if res:
            print(res)
            break
          if attempt < MAX_TRIES:
            if verbose:
              print(f"  (continuing conversation, attempt {attempt + 1}/{MAX_TRIES})")
        except Exception as e:
          last_error = e
          if verbose:
            print(f"  Error on attempt {attempt}/{MAX_TRIES}")
          if attempt < MAX_TRIES:
            continue
          else:
            print(f"Error after {MAX_TRIES} attempts: {e}")
            # remove last msg from messsages to avoid corruption. smh docs suggest lol
            messages.pop()
            break
      else:
        if last_error:
          print(f"Failed after {MAX_TRIES} attempts. Last error: {last_error}")
        else:
          print(f"No response after {MAX_TRIES} attempts.")

    except KeyboardInterrupt:
      print("\nInterrupted. Goodbye!")
      sys.exit(0)
    except EOFError:
      print("\nGoodbye!")
      sys.exit(0)


def generate_content(client, messages, verbose) -> str | None:
  response: types.GenerateContentResponse = client.models.generate_content(
    model=GEMINI_MODEL,
    contents=messages,
    config=types.GenerateContentConfig(
      tools=[available_functions], system_instruction=system_prompt
    ),
  )

  if response.candidates:
    for candidate in response.candidates:
      messages.append(candidate.content)

  if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")  # pyright: ignore[reportOptionalMemberAccess]
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")  # pyright: ignore[reportOptionalMemberAccess]

  if not response.function_calls:
    return response.text

  fn_resp: list[types.Part] = []
  for fn_call in response.function_calls:
    result: types.Content = call_function(fn_call, verbose)
    if not result.parts or not result.parts[0].function_response:  # pyright: ignore[reportOptionalSubscript]
      raise Exception("empty function call result.")
    fn_resp.append(result.parts[0])  # pyright: ignore[reportOptionalSubscript, reportArgumentType]
    if verbose:
      print(f"-> {result.parts[0].function_response.response}")  # pyright: ignore[reportOptionalSubscript]

  if not fn_resp:
    raise Exception("no function responses generated, exiting.")
  for fn in fn_resp:
    messages.append(
      types.Content(
        role="user", parts=[types.Part(function_response=fn.function_response)]
      )
    )

    # recursive call to continue conversation
    return generate_content(client, messages, verbose)


if __name__ == "__main__":
  main()

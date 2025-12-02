WORKING_DIR: str = "./calculator"

GEMINI_MODEL: str = "gemini-2.0-flash-001"
MAX_CHARS_TO_READ: int = 10000
MAX_TRIES: int = 25
TIMEOUT_SECS: int = 30
BINARY_ALLOWLIST: list[str] = [
  "python3",
  "node",
  "npm",
  "pnpm",
  "yarn",
  "go",
  "cargo",
  "pytest",
  "uv",
  "bash",
]


HEADER: str = """
  █ ▄   ▄ ▄▄▄▄  ▗▞▀▚▖▄   ▄
  █ █   █ █   █ ▐▛▀▀▘█   █
  █  ▀▀▀█ █   █ ▝▚▄▄▖ ▀▀▀█
  █ ▄   █            ▄   █
    ▀▀▀              ▀▀▀
"""

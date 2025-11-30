# Lyney - AI Codihhn Agent

An interactive AI-powered coding assistant built with Google's Gemini API. Lyney helps you with code-related tasks through natural language conversations, allowing you to focus on higher-level problem-solving rather than manual coding.

## Overview

Lyney is a command-line AI agent that uses Google's Gemini models to understand your coding requests and execute them using a set of built-in functions. It maintains conversation context and can perform file operations, code execution, and more—all while ensuring security by constraining operations to a specified working directory.

## Features

### Core Capabilities

- **Interactive CLI Interface**: Clean, user-friendly command-line interface with a custom ASCII header
- **Natural Language Processing**: Communicate with the agent using plain English
- **Function Calling**: The agent can autonomously call functions to:
  - **Read Files**: Read and display file contents (up to 10,000 characters per file, ref: flash-2.0 model)
  - **List Files**: Explore directory structures with file sizes and metadata
  - **Write Files**: Create or modify files with full content control
  - **Execute Python Files**: Run Python scripts with optional command-line arguments
- **Conversation Memory**: Maintains context across multiple interactions
- **Error Handling**: Robust retry mechanism (up to 25 attempts) with detailed error reporting
- **Verbose Mode**: Optional detailed logging for debugging and monitoring

### Security Features

- **Path Validation**: All file operations are restricted to a configurable working directory
- **Sandboxed Execution**: Python file execution is constrained to the working directory
- **Timeout Protection**: File execution has a 30-second timeout to prevent hanging processes

## Getting Started

### Prerequisites

- Python 3.13 or higher
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:Sarthak2143/lyney.git
   cd lyney/
   ```

2. Install dependencies using `uv`:
   ```bash
   # Using uv
   uv sync

3. Set up your environment:
   ```bash
   # Create a .env file in the project root
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

### Running the Agent

Start the agent with:
```bash
uv run main.py
```

For verbose output (shows token usage and function call details):
```bash
uv run main.py --verbose
```

### Usage Examples

Once the agent is running, you can interact with it naturally:

```
> List all files in the current directory
> Read the contents of main.py
> Create a new file called test.py with a hello world function
> Run the calculator.py file with arguments 5 3
> Modify the render.py file to add error handling
```

To exit, type `exit` or `quit`, or press `Ctrl+C`.

## Project Structure

```
lyney/
├── main.py                 # Main entry point and conversation loop
├── config.py              # Configuration settings (model, paths, limits)
├── prompts.py             # System prompt and agent instructions
├── schemas.py             # Function declarations and call routing
└── functions/             # Available function implementations
    ├── get_file_content.py    # Read file contents
    ├── get_files_info.py      # List directory contents
    ├── write_file.py          # Write/create files
    ├── run_file.py            # Execute Python files
    └── utils.py               # Path validation utilities
```

## Configuration

Edit `config.py` to customize the agent:

```python
GEMINI_MODEL: str = "gemini-2.0-flash-001"  # Gemini model to use
MAX_CHARS_TO_READ: int = 10000              # Max characters per file read
MAX_TRIES: int = 25                          # Max retry attempts
WORKING_DIR: str = "./calculator"           # Working directory for operations
```

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

## Available Functions

The agent has access to the following functions:

### `get_file_content(file_path: str)`
Reads the contents of a file within the working directory. Files larger than 10,000 characters are truncated with a notice.

### `get_files_info(directory: str = ".")`
Lists all files and directories in the specified path, showing:
- File/directory names
- File sizes in bytes
- Whether each item is a directory

### `write_file(file_path: str, content: str)`
Writes content to a file. Creates the file if it doesn't exist, and creates parent directories as needed.

### `run_python_file(file_path: str, args: list[str] | None = None)`
Executes a Python file with optional command-line arguments. Returns:
- STDOUT output
- STDERR output
- Exit code

Execution is limited to 30 seconds and runs within the working directory context.

## Security Considerations

- **Path Validation**: All file paths are validated to ensure they remain within the working directory, preventing directory traversal attacks
- **Sandboxed Execution**: Python files are executed with a timeout and within the working directory scope
- **No Network Access**: The agent cannot make network requests or access external resources
- **Read Limits**: File reading is limited to prevent memory issues with large files

## Customization

### Modifying the System Prompt

Edit `prompts.py` to change the agent's behavior, personality, or instructions. The system prompt defines:
- How the agent responds to requests
- What operations it can perform
- Its communication style
- Safety guidelines

### Adding New Functions

To add new capabilities:

1. Create a new function in `functions/` directory
2. Define its schema using `types.FunctionDeclaration`
3. Add the schema to `available_functions` in `schemas.py`
4. Add the function to the `functions` dictionary in `call_function()`

## Troubleshooting

### Common Issues

**"Error: Cannot read/write file as it is outside the permitted working directory"**
- Ensure the file path is relative to the working directory specified in `config.py`
- Check that you're not using absolute paths or `..` to escape the directory

**"No response after X attempts"**
- Check your API key is valid and set in the `.env` file
- Verify you have internet connectivity
- Try running with `--verbose` to see detailed error messages

**"Execution timed out"**
- The script you're running may be taking too long
- Consider optimizing the script or increasing the timeout in `run_file.py`

---

**Note**: This is an AI coding assistant tool. Always review generated code before using it in production environments.

credits for claude to write this md file, im too retarded to do on my own.
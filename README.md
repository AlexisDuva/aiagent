# aiagent

A minimal AI coding agent. It sends your prompt to an LLM (via the
[OpenRouter](https://openrouter.ai) API using the OpenAI client) together with a
set of function-calling tools, then executes the tool calls the model requests
in an agent loop (up to 5 iterations per run).

## Tools available to the agent

All tool calls are scoped to a working directory (`./calculator` by default,
set in `functions/call_function.py`):

| Tool | Description |
| --- | --- |
| `get_files_info` | List files and directories |
| `get_file_content` | Read the contents of a file |
| `write_file` | Write or overwrite a file |
| `run_python_file` | Execute a Python file with optional arguments |

The repo also ships a sample `calculator/` package that the agent operates on.

## ⚠️ Warning — this project can be dangerous

**This agent executes actions decided by an LLM on your machine.** It can:

- **Delete or overwrite important files** via `write_file`
- **Execute unwanted or harmful programs** via `run_python_file`

The path checks only confine tools to the configured working directory; they do
**not** make execution safe. A malicious prompt, a prompt-injection in a file
the agent reads, or simply a model mistake can cause data loss or arbitrary code
execution. Run it only on throwaway data, ideally inside a container or VM, and
review the working directory setting before each run.

## Requirements

- Python >= 3.12
- An OpenRouter API key

## Setup

```bash
# with uv (recommended)
uv sync

# or with pip
pip install -e .
```

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=your_key_here
```

## Launch

```bash
uv run main.py "your prompt here"

# or, if the environment is already active
python main.py "your prompt here"

# verbose output (messages, per-call details)
uv run main.py "your prompt here" --verbose
```

Example:

```bash
uv run main.py "list the files in the calculator package and run its tests"
```

## Running the tests

The `test_*.py` files are standalone scripts that print their results:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```

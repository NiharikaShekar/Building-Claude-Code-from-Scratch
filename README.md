# AI Coding Agent

An agentic AI system powered by **Google Gemini 2.5 Flash** that autonomously reasons, plans, and executes actions to solve coding tasks — similar to how tools like Claude Code operate under the hood.

## How It Works

The agent follows an **agentic loop**: it receives a natural language prompt, decides which tools to call, executes them, observes the results, and keeps iterating until it produces a final answer — all without human intervention.

```
User Prompt
    │
    ▼
Gemini 2.5 Flash (reasons + plans)
    │
    ▼
Tool Call (get files, read code, run script, write file)
    │
    ▼
Tool Result fed back to model
    │
    ▼
Repeat until final answer is produced
```

The agent operates within a sandboxed working directory (`calculator/`) and has path traversal protection built in — it cannot access files outside its permitted scope.

## Tools Available to the Agent

| Tool | Description |
|------|-------------|
| `get_files_info` | List files and directories with metadata |
| `get_file_content` | Read file contents (with configurable character limit) |
| `run_python_file` | Execute Python scripts and capture stdout/stderr |
| `write_file` | Write or overwrite files in the working directory |

These tools are defined as structured **function declarations** passed to Gemini's tool-use API, enabling the model to call them natively as part of its reasoning process.

## Project Structure

```
building_ai_agent/
├── main.py              # Entry point — runs the agentic loop
├── prompts.py           # System prompt defining agent behavior
├── call_functions.py    # Tool dispatcher and function registry
├── config.json          # Configuration (e.g. max file read size)
├── functions/
│   ├── get_file_content.py   # Read file tool
│   ├── get_files_info.py     # List files tool
│   ├── run_python_file.py    # Execute Python tool
│   └── write_file.py         # Write file tool
└── calculator/          # Sandboxed project the agent operates on
    ├── main.py
    ├── tests.py
    └── pkg/
        ├── calculator.py
        └── render.py
```

## Getting Started

### Prerequisites

- Python 3.12+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

### Installation

```bash
# Clone the repo
git clone https://github.com/NiharikaShekar/building_ai_agent.git
cd building_ai_agent

# Install dependencies
uv sync
# or: pip install google-genai python-dotenv
```

### Configuration

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_api_key_here
```

### Usage

```bash
python main.py "your task here"
```

**Examples:**

```bash
# Ask the agent to explore the codebase
python main.py "list all files in the project"

# Ask it to read and explain code
python main.py "read the calculator.py file and explain how it works"

# Ask it to run tests
python main.py "run the tests and tell me if they pass"

# Ask it to fix a bug or add a feature
python main.py "add a modulo operator to the calculator"
```

Add `--verbose` to see every tool call the agent makes:

```bash
python main.py "run the tests" --verbose
```

## Key Design Decisions

- **Agentic loop with 20-iteration cap** — prevents runaway execution while giving the model enough steps to complete multi-hop tasks
- **Sandboxed execution** — all file and execution tools validate paths using `os.path.commonpath` to prevent directory traversal
- **Structured tool schemas** — tools are declared with typed JSON schemas so Gemini can call them reliably with correct arguments
- **Subprocess isolation** — Python files are run as subprocesses with a 30-second timeout, keeping the agent environment clean

## Tech Stack

- **LLM:** Google Gemini 2.5 Flash
- **SDK:** `google-genai`
- **Python:** 3.12+

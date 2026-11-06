# LLM Ticket Classifier

A Python prototype exploring how large language models (LLMs) can analyze free-text workplace complaints and turn them into structured support-ticket information.

The repository contains two independent experiments:

- **OpenAI classifier:** Uses the OpenAI API and Structured Outputs (JSON Schema) to identify one or more tickets, assign a department/category/subcategory, and generate a title, priority, and summary.
- **Ollama classifier:** Uses a locally hosted **Qwen2.5 3B** model through Ollama to explore basic complaint analysis without an external API key.

These are command-line prototypes, **not production integrations** with a ticket-management application.

## Repository structure

```text
llm-ticket-classifier/
├── openai-classifier/
│   └── main.py
├── ollama-classifier/
│   └── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The filenames above are the suggested public repository layout.

## Features

### OpenAI classifier

- Accepts a free-text complaint from the terminal.
- Uses a predefined **Department → Category → Subcategory** hierarchy in its system prompt.
- Requests a structured response with an `is_valid` flag and a list of tickets.
- Generates a **title, department, category, subcategory, priority, and summary** for each ticket.
- Instructs the model to separate distinct issues into multiple tickets.
- Uses OpenAI Structured Outputs with a strict JSON Schema, including a priority enum (`Low`, `Medium`, `High`).
- Prints an escalation message for tickets assigned **High** priority.

**Validation note:** JSON Schema constrains the response structure, but it does not independently prove that the model chose the correct category or priority. The script checks for the top-level fields; classification accuracy still requires testing.

### Ollama classifier

- Runs **Qwen2.5 3B** locally using `ollama.chat()`.
- Prompts the model to return JSON containing `category`, `priority`, `sentiment`, and `summary`.
- Parses the model's response as JSON.

The current Ollama script is an earlier experiment: its display and validation logic is mostly commented out, and it does **not** implement the OpenAI version's full ticket hierarchy or strict output schema.

## Requirements

- Python 3.10+ (recommended)
- Dependencies listed in `requirements.txt`:
  - `openai`
  - `python-dotenv`
  - `ollama`
- An **OpenAI API key** for the OpenAI version
- A running **Ollama** service with the `qwen2.5:3b` model for the local version

## Setup

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/YOUR_USERNAME/llm-ticket-classifier.git
cd llm-ticket-classifier
python -m venv venv
```

Activate it:

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Run the OpenAI classifier

1. Create a `.env` file in the repository root (or copy `.env.example`).
2. Add your key:

   ```dotenv
   OPENAI_API_KEY=your_api_key_here
   ```
3. In `openai-classifier/main.py`, load the root `.env` explicitly if you run the script from different working directories:

   ```python
   from pathlib import Path
   from dotenv import load_dotenv

   load_dotenv(Path(__file__).resolve().parent.parent / ".env")
   ```
4. Run:

   ```bash
   python openai-classifier/main.py
   ```

The OpenAI script uses the model identifier configured in its `main.py`. Ensure that the identifier is available to your account before running it.

### Run the Ollama classifier

Install Ollama, start its service, and download the model:

```bash
ollama pull qwen2.5:3b
```

Then run:

```bash
python ollama-classifier/main.py
```

**No OpenAI API key is required for the local Ollama version.**

## Example: multiple issues in one complaint

**Input** (original test, including typos):

```text
i am unable to use s n 5 key and the mouse of keyboard also unable to give prints to pronter
```

**Observed OpenAI classifier output (abridged):**

| Ticket | Department | Category | Subcategory | Priority |
|---|---|---|---|---|
| Keyboard Malfunction | IT, Systems & Digital | Hardware | Keyboard | Medium |
| Mouse Malfunction | IT, Systems & Digital | Hardware | Mouse | Medium |
| Printer Printing Issue | IT, Systems & Digital | Hardware | Printer | Medium |

The classifier extracted three tickets from a single informal complaint. This example illustrates behavior in one test run, **not a measured accuracy or reliability claim**.

## OpenAI vs. Ollama

| Aspect | OpenAI version | Ollama version |
|---|---|---|
| Model access | OpenAI API | Local Ollama service |
| API key | Required | Not required for local use |
| Output | Strict JSON Schema structure | Prompt-requested JSON |
| Multiple tickets | Prompted and represented as a ticket list | Not implemented in the current script |
| Classification | Department / Category / Subcategory | Basic category field |
| Current status | More developed prototype | Early experiment |

## Limitations and possible improvements

- The classification hierarchy is defined in the prompt; category membership is not independently verified against an external taxonomy.
- An LLM can still misinterpret ambiguous complaints or assign an incorrect priority.
- The scripts are interactive terminal programs, not REST APIs or deployed services.
- Add a set of labeled test complaints to evaluate classification accuracy, invalid-input handling, and multi-ticket extraction.
- Add robust exception handling for unavailable models, API errors, and malformed responses.
- Consider implementing the same output contract for both models to make comparisons more meaningful.

## Security

Never commit API keys or your local virtual environment. Suggested `.gitignore` entries:

```gitignore
.env
venv/
.venv/
__pycache__/
*.py[cod]
```

Use `.env.example` with placeholder values only. Before publishing, review prompts and category lists for any client-specific or confidential information.

## Project status

**Prototype / learning project.** The goal is to explore practical LLM integration, structured responses, and local inference for support-ticket analysis.

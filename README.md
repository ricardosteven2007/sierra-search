# Sierra Search

A small search orchestrator that runs multiple search APIs (Tavily + Brave)
in parallel and selects the best answer.

## What this does
- Sends the same question to multiple search APIs
- Normalizes their outputs into the same format
- Picks the best result based on simple scoring rules
- Designed to be expandable (add more adapters easily)

## Project Structure

```text
sierra-search/
├── main.py
├── adapters/
│   ├── tavily_adapter.py
│   └── brave_adapter.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your API keys:

```text
TAVILY_API_KEY=your_tavily_api_key
BRAVE_API_KEY=your_brave_api_key
```

4. Run Sierra Search:

```bash
python main.py
```

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
│   ├── tavily.py
│   └── brave.py
├── .gitignore
└── README.md

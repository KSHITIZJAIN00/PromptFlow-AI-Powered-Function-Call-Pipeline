 AI-Powered Function Call Pipeline

## Overview

**PromptFlow** is an AI-powered natural language pipeline that interprets user queries and converts them into a structured sequence of function calls. 
It utilizes a language model (FLAN-Alpaca) to understand intents such as invoice summarization, calendar event creation, email sending, and file writing.

This project is implemented in Python using HuggingFace Transformers and is designed to be modular, interpretable, and testable.


##  Project Workflow

### 1 **User Input**
The user enters a natural language query, like:

> "Get invoices for March, summarize them, and email me the report."

### 2. **Planning with AI**
The query is passed into the `ModelEngine` class, which:
- Constructs a prompt for the model.
- Calls a text2text pipeline using the `flan-alpaca-large` model.
- Expects a JSON output (sequence of function calls).

If the model returns malformed output, a fallback parser uses pattern matching to reconstruct the plan.

### 3. **Generated Output**
The output is a structured JSON plan such as:

```json
[
  {
    "function": "get_invoices",
    "args": { "month": "March" }
  },
  {
    "function": "summarize_invoices",
    "args": { "invoices": "<output_of_get_invoices>" }
  },
  {
    "function": "send_email",
    "args": {
      "to": "me@example.com",
      "subject": "Invoice Summary",
      "body": "<output_of_summarize_invoices>"
    }
  }
]

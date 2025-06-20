## AI-Powered Function Call Pipeline
## Demonstration - 


https://github.com/user-attachments/assets/8f822289-cda1-4f7b-944a-8d743ceab66f


## Output Query - 
![Screenshot 2025-06-21 022750](https://github.com/user-attachments/assets/13cbbb47-0aca-4a62-be17-c1687393515e)
![Screenshot 2025-06-21 022759](https://github.com/user-attachments/assets/3b0e317f-ea3c-43d8-81fb-11e370b1161c)
![Screenshot 2025-06-21 022809](https://github.com/user-attachments/assets/0cd6f698-26bd-451d-a81f-f4dbd6691faa)

## Overview


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
